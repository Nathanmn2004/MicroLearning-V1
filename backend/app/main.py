from contextlib import asynccontextmanager
from secrets import token_urlsafe

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db, init_db
from .email_service import send_confirmation_email
from .models import Subscriber
from .scheduler import start_scheduler, stop_scheduler

settings = get_settings()


class SubscribeRequest(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    email: EmailStr


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(title="Microaprendizagem API", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/subscribe")
def subscribe(payload: SubscribeRequest, db: Session = Depends(get_db)) -> dict:
    email = payload.email.lower()
    subscriber = db.query(Subscriber).filter(Subscriber.email == email).first()

    if subscriber:
        if subscriber.confirmed:
            return {"success": True, "message": "Assinatura já confirmada."}

        subscriber.name = payload.name
        subscriber.confirm_token = token_urlsafe(32)
        subscriber.unsubscribe_token = token_urlsafe(32)
    else:
        subscriber = Subscriber(
            name=payload.name,
            email=email,
            confirm_token=token_urlsafe(32),
            unsubscribe_token=token_urlsafe(32),
        )
        db.add(subscriber)

    db.commit()
    db.refresh(subscriber)
    send_confirmation_email(subscriber)
    return {"success": True, "message": "Confira seu email para confirmar a assinatura."}


@app.get("/api/confirm/{token}")
def confirm(token: str, db: Session = Depends(get_db)) -> dict:
    subscriber = db.query(Subscriber).filter(Subscriber.confirm_token == token).first()
    if subscriber is None:
        raise HTTPException(status_code=404, detail="Token inválido.")

    subscriber.confirmed = True
    db.commit()
    return {"success": True}


@app.get("/api/unsubscribe/{token}")
def unsubscribe(token: str, db: Session = Depends(get_db)) -> dict:
    subscriber = db.query(Subscriber).filter(Subscriber.unsubscribe_token == token).first()
    if subscriber is None:
        raise HTTPException(status_code=404, detail="Token inválido.")

    db.delete(subscriber)
    db.commit()
    return {"success": True}

