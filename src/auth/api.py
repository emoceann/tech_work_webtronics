from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.service.auth_logic import register_user, get_current_user, login_user
from src.profile.models import UserIn, UserOut

router = APIRouter(prefix="/auth")


@router.post("/reg")
async def reg_user(data: UserIn):
    return await register_user(data)


@router.post("/token")
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_user(form_data)


@router.get("/me")
async def get_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
