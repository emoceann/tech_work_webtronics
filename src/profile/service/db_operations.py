from src.profile.dao import User
from src.profile.models import UserIn


async def create_user(user: UserIn):
    return await User.create(**user.dict())


async def exists_check(username: str):
    return await User.exists(username=username)


async def get_user_by_id(user_id: int):
    return await User.get_or_none(id=user_id)


async def get_user_by_username(username: str):
    return await User.get_or_none(username=username)
