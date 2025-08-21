from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from typing import Dict

from ..db import get_session
from ..models import User
from ..security import (
    create_access_token,
    get_password_hash,
    verify_password,
    get_current_user,
)

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EffectConfig(BaseModel):
    enabled: bool = True
    intensity: float = 1.0


class Preferences(BaseModel):
    effectsEnabled: bool = True
    fontSize: int = 16
    brightness: float = 1.0
    adaptiveBrightness: bool = False
    effects: Dict[str, EffectConfig] = Field(
        default_factory=lambda: {
            "motion": EffectConfig(),
            "color": EffectConfig(),
        }
    )


@router.post("/register", response_model=Token)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(email=user.email, hashed_password=get_password_hash(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    token = create_access_token({"sub": str(db_user.id)})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"sub": str(db_user.id)})
    return Token(access_token=token)


@router.get("/", response_model=list[User])
def read_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/me/preferences", response_model=Preferences)
def get_preferences(current_user: User = Depends(get_current_user)):
    return Preferences(**(current_user.preferences or {}))


@router.put("/me/preferences", response_model=Preferences)
def update_preferences(
    prefs: Preferences,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    current_user.preferences = prefs.model_dump()
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return Preferences(**current_user.preferences)
