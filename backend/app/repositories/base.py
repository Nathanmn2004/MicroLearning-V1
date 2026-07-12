from collections.abc import Mapping
from typing import Any

from supabase import Client

from app.repositories.supabase_client import get_supabase_admin_client


class SupabaseRepository:
    def __init__(self, table_name: str, client: Client | None = None) -> None:
        self.table_name = table_name
        self.client = client or get_supabase_admin_client()

    def list(self, limit: int = 100, offset: int = 0) -> list[dict[str, Any]]:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .range(offset, offset + limit - 1)
            .execute()
        )
        return response.data

    def get(self, record_id: str) -> dict[str, Any] | None:
        response = (
            self.client.table(self.table_name)
            .select("*")
            .eq("id", record_id)
            .limit(1)
            .execute()
        )
        return response.data[0] if response.data else None

    def create(self, data: Mapping[str, Any]) -> dict[str, Any]:
        response = self.client.table(self.table_name).insert(dict(data)).execute()
        return response.data[0]

    def update(self, record_id: str, data: Mapping[str, Any]) -> dict[str, Any]:
        response = (
            self.client.table(self.table_name)
            .update(dict(data))
            .eq("id", record_id)
            .execute()
        )
        return response.data[0]
