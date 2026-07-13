import hashlib
import hmac
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, HTTPException, Request

from app.core.config import settings
from app.repositories.supabase_client import get_supabase_admin_client


router = APIRouter(prefix="/webhooks", tags=["webhooks"])

ACTIVE_EVENTS = {
    "purchase_approved",
    "subscription_created",
    "subscription_renewed",
}
INACTIVE_EVENTS = {
    "purchase_refused": "pending",
    "subscription_renewal_refused": "overdue",
    "subscription_canceled": "cancelled",
    "subscription_cancelled": "cancelled",
    "refund": "refunded",
    "chargeback": "refunded",
}


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _normalize_email(value: Any) -> str | None:
    text = _normalize_text(value)
    return text.lower() if text else None


def _normalize_phone(value: Any) -> str | None:
    text = _normalize_text(value)
    if not text:
        return None
    phone = "".join(char for char in text if char.isdigit() or char == "+")
    return phone or None


def _deep_get(data: dict[str, Any], paths: tuple[str, ...]) -> Any:
    for path in paths:
        current: Any = data
        for part in path.split("."):
            if isinstance(current, dict) and part in current:
                current = current[part]
                continue
            current = None
            break
        if current not in (None, ""):
            return current
    return None


def _event_type(payload: dict[str, Any]) -> str:
    event = _deep_get(
        payload,
        (
            "event",
            "event_type",
            "type",
            "data.event",
            "data.event_type",
            "data.type",
            "webhook_event_type",
        ),
    )
    return _normalize_text(event) or "unknown"


def _provider_event_id(payload: dict[str, Any]) -> str | None:
    return _normalize_text(
        _deep_get(
            payload,
            (
                "id",
                "event_id",
                "webhook_id",
                "transaction.id",
                "transaction_id",
                "sale.id",
                "sale_id",
                "order.id",
                "order_id",
                "data.id",
                "data.transaction.id",
                "data.transaction_id",
                "data.sale.id",
                "data.sale_id",
                "data.order.id",
                "data.order_id",
            ),
        )
    )


def _customer_data(payload: dict[str, Any]) -> dict[str, str | None]:
    name = _normalize_text(
        _deep_get(
            payload,
            (
                "customer.name",
                "customer.full_name",
                "client.name",
                "buyer.name",
                "user.name",
                "data.customer.name",
                "data.customer.full_name",
                "data.client.name",
                "data.buyer.name",
                "data.user.name",
            ),
        )
    )
    email = _normalize_email(
        _deep_get(
            payload,
            (
                "customer.email",
                "client.email",
                "buyer.email",
                "user.email",
                "email",
                "data.customer.email",
                "data.client.email",
                "data.buyer.email",
                "data.user.email",
                "data.email",
            ),
        )
    )
    phone = _normalize_phone(
        _deep_get(
            payload,
            (
                "customer.phone",
                "customer.phone_number",
                "client.phone",
                "buyer.phone",
                "user.phone",
                "phone",
                "whatsapp",
                "data.customer.phone",
                "data.customer.phone_number",
                "data.client.phone",
                "data.buyer.phone",
                "data.user.phone",
                "data.phone",
                "data.whatsapp",
            ),
        )
    )
    customer_id = _normalize_text(
        _deep_get(
            payload,
            (
                "customer.id",
                "customer_id",
                "client.id",
                "buyer.id",
                "user.id",
                "data.customer.id",
                "data.customer_id",
                "data.client.id",
                "data.buyer.id",
                "data.user.id",
            ),
        )
    )
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "provider_customer_id": customer_id,
    }


def _subscription_data(payload: dict[str, Any], event_type: str) -> dict[str, Any]:
    subscription_id = _normalize_text(
        _deep_get(
            payload,
            (
                "subscription.id",
                "subscription_id",
                "data.subscription.id",
                "data.subscription_id",
                "contract.id",
                "contract_id",
                "data.contract.id",
                "data.contract_id",
            ),
        )
    )
    plan_name = _normalize_text(
        _deep_get(
            payload,
            (
                "product.name",
                "product.title",
                "offer.name",
                "plan.name",
                "data.product.name",
                "data.product.title",
                "data.offer.name",
                "data.plan.name",
            ),
        )
    )

    if event_type in ACTIVE_EVENTS:
        status = "active"
    else:
        status = INACTIVE_EVENTS.get(event_type, "pending")

    data: dict[str, Any] = {
        "provider": "cakto",
        "provider_subscription_id": subscription_id,
        "plan_name": plan_name,
        "status": status,
        "last_verified_at": _now_iso(),
    }
    if event_type == "subscription_created":
        data["started_at"] = _now_iso()
    if status in {"cancelled", "refunded"}:
        data["cancelled_at"] = _now_iso()
    return data


def _signature_is_valid(raw_body: bytes, request: Request) -> bool:
    secret = settings.cakto_webhook_secret
    if not secret:
        return True

    candidates = [
        request.headers.get("x-cakto-webhook-secret"),
        request.headers.get("x-cakto-secret"),
        request.headers.get("x-webhook-secret"),
        request.query_params.get("secret"),
    ]

    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        candidates.append(auth_header[7:].strip())

    if any(hmac.compare_digest(secret, value) for value in candidates if value):
        return True

    signature = request.headers.get("x-cakto-signature") or request.headers.get(
        "x-webhook-signature"
    )
    if not signature:
        return False

    received = signature.removeprefix("sha256=").strip()
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, received)


def _find_existing_subscriber(
    client: Any,
    customer: dict[str, str | None],
) -> dict[str, Any] | None:
    lookups = (
        ("provider_customer_id", customer.get("provider_customer_id")),
        ("email", customer.get("email")),
        ("phone", customer.get("phone")),
    )
    for field, value in lookups:
        if not value:
            continue
        response = (
            client.table("subscribers")
            .select("*")
            .eq(field, value)
            .limit(1)
            .execute()
        )
        if response.data:
            return response.data[0]
    return None


def _upsert_subscriber(client: Any, customer: dict[str, str | None]) -> dict[str, Any] | None:
    if not any(customer.values()):
        return None

    existing = _find_existing_subscriber(client, customer)
    data = {key: value for key, value in customer.items() if value}
    data["source"] = "cakto"

    if existing:
        response = (
            client.table("subscribers")
            .update(data)
            .eq("id", existing["id"])
            .execute()
        )
        return response.data[0]

    response = client.table("subscribers").insert(data).execute()
    return response.data[0]


def _upsert_subscription(
    client: Any,
    subscriber: dict[str, Any] | None,
    customer: dict[str, str | None],
    subscription: dict[str, Any],
) -> dict[str, Any] | None:
    if not subscriber:
        return None

    subscription["subscriber_id"] = subscriber["id"]
    if customer.get("provider_customer_id"):
        subscription["provider_customer_id"] = customer["provider_customer_id"]

    provider_subscription_id = subscription.get("provider_subscription_id")
    existing: dict[str, Any] | None = None
    if provider_subscription_id:
        response = (
            client.table("subscriptions")
            .select("*")
            .eq("provider", "cakto")
            .eq("provider_subscription_id", provider_subscription_id)
            .limit(1)
            .execute()
        )
        if response.data:
            existing = response.data[0]

    if not existing:
        response = (
            client.table("subscriptions")
            .select("*")
            .eq("provider", "cakto")
            .eq("subscriber_id", subscriber["id"])
            .limit(1)
            .execute()
        )
        if response.data:
            existing = response.data[0]

    if existing:
        response = (
            client.table("subscriptions")
            .update({key: value for key, value in subscription.items() if value is not None})
            .eq("id", existing["id"])
            .execute()
        )
        return response.data[0]

    response = client.table("subscriptions").insert(
        {key: value for key, value in subscription.items() if value is not None}
    ).execute()
    return response.data[0]


@router.post("/cakto")
async def cakto_webhook(request: Request) -> dict[str, Any]:
    raw_body = await request.body()
    if not _signature_is_valid(raw_body, request):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    try:
        payload = await request.json()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON payload") from exc

    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="Payload must be a JSON object")

    client = get_supabase_admin_client()
    event_type = _event_type(payload)
    provider_event_id = _provider_event_id(payload)

    existing_event = None
    if provider_event_id:
        response = (
            client.table("payment_events")
            .select("*")
            .eq("provider_event_id", provider_event_id)
            .limit(1)
            .execute()
        )
        existing_event = response.data[0] if response.data else None

    if existing_event and existing_event.get("processed"):
        return {
            "ok": True,
            "duplicate": True,
            "event_type": event_type,
        }

    if existing_event:
        payment_event = existing_event
    else:
        response = client.table("payment_events").insert(
            {
                "event_type": event_type,
                "provider_event_id": provider_event_id,
                "payload": payload,
                "processed": False,
            }
        ).execute()
        payment_event = response.data[0]

    customer = _customer_data(payload)
    subscriber = _upsert_subscriber(client, customer)
    subscription = _upsert_subscription(
        client,
        subscriber,
        customer,
        _subscription_data(payload, event_type),
    )

    update_data: dict[str, Any] = {
        "processed": True,
        "processed_at": _now_iso(),
    }
    if subscriber:
        update_data["subscriber_id"] = subscriber["id"]

    client.table("payment_events").update(update_data).eq("id", payment_event["id"]).execute()

    return {
        "ok": True,
        "event_type": event_type,
        "subscriber_id": subscriber["id"] if subscriber else None,
        "subscription_id": subscription["id"] if subscription else None,
    }
