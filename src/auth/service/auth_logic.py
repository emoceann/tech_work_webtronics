from datetime import timedelta, datetime
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError
from passlib.hash import bcrypt
import jwt

from src.auth.models import TokenData
from src.auth.service.email_verify import verfiy_email_request
from src.profile.dao import User
from src.profile.models import UserIn, UserOut
from src.profile.service.db_operations import exists_check, create_user, get_user_by_id, get_user_by_username
from src.settings import get_settings

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def register_user(user: UserIn):
    if await exists_check(user.username):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not await verfiy_email_request(user.email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user.password = hash_password(password=user.password)
    user = await create_user(user)
    access_token = create_access_token({"user_id": user.id})
    return TokenData(access_token=access_token, token_type="bearer")


async def login_user(form_data):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"user_id": user.id}
    )
    return TokenData(access_token=access_token, token_type="bearer")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload: dict = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Expired token")
    user = await get_user_by_id(payload["user_id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    return UserOut.from_orm(user)


def hash_password(password: str):
    return bcrypt.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def authenticate_user(username: str, password: str) -> User | bool:
    user = await get_user_by_username(username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)
