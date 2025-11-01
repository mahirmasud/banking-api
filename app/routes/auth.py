from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserCreate, Token, LoginIn, UserOut
from app.core.memory import get_memory
from app.core.security import hash_password, verify_password, create_access_token
from datetime import datetime, timedelta

router = APIRouter(prefix="", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(user_in: UserCreate):
    mem = get_memory()
    async with mem.lock:
        if user_in.username in mem.users:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
        mem.users[user_in.username] = {
            "password_hash": hash_password(user_in.password),
            "full_name": user_in.full_name,
            "created_at": datetime.utcnow().isoformat()
        }
    return {"username": user_in.username, "full_name": user_in.full_name}

@router.post("/login", response_model=Token)
async def login(payload: LoginIn):
    mem = get_memory()
    user = mem.users.get(payload.username)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=payload.username, expires_delta=timedelta(hours=24))
    return {"access_token": token, "token_type": "bearer"}
