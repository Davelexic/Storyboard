from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, validator
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
from ..utils.sanitization import (
    sanitize_email,
    sanitize_password,
    SanitizationError,
)
from ..exceptions import (
    ValidationError,
    AuthenticationError,
    ConflictError,
    ResourceNotFoundError
)

router = APIRouter(prefix="/users", tags=["users"])


class UserCreate(BaseModel):
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        try:
            return sanitize_email(v)
        except SanitizationError as e:
            raise ValueError(str(e))
    
    @validator('password')
    def validate_password(cls, v):
        try:
            return sanitize_password(v, min_length=8)
        except SanitizationError as e:
            raise ValueError(str(e))


class UserLogin(BaseModel):
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        try:
            return sanitize_email(v)
        except SanitizationError as e:
            raise ValueError(str(e))
    
    @validator('password')
    def validate_password(cls, v):
        try:
            return sanitize_password(v, min_length=8)
        except SanitizationError as e:
            raise ValueError(str(e))


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
    
    @validator('fontSize')
    def validate_font_size(cls, v):
        if not isinstance(v, int) or v < 8 or v > 72:
            raise ValueError("Font size must be between 8 and 72")
        return v
    
    @validator('brightness')
    def validate_brightness(cls, v):
        if not isinstance(v, (int, float)) or v < 0.1 or v > 2.0:
            raise ValueError("Brightness must be between 0.1 and 2.0")
        return float(v)


@router.post("/register", response_model=Token)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == user.email)).first()
    if existing:
        raise ConflictError("Email already registered", conflict_type="email_exists")
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
        raise AuthenticationError("Incorrect email or password")
    token = create_access_token({"sub": str(db_user.id)})
    return Token(access_token=token)


@router.get("/", response_model=list[User])
def read_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise ResourceNotFoundError("User not found", resource_type="user", resource_id=str(user_id))
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
    current_user.preferences = prefs.dict()
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return Preferences(**current_user.preferences)
