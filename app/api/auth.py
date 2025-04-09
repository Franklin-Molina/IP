from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.crud.user import create_user, get_user_by_username, verify_password
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret"  # En producción, usar variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/auth/register", response_model=TokenResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario y devuelve un token.
    """
    existing = get_user_by_username(db, user_data.username)
    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya existe")
    user = create_user(db, user_data.username, user_data.password)
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/auth/login", response_model=TokenResponse)
def login(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Autentica un usuario y devuelve un token.
    """
    user = get_user_by_username(db, user_data.username)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

def create_access_token(data: dict) -> str:
    """
    Crea un JWT con expiración.

    Args:
        data (dict): Datos a incluir en el token.

    Returns:
        str: JWT codificado.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
