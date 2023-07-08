from fastapi import APIRouter, Depends, status

from src.auth.service.auth_logic import get_current_user
from src.posts.models import PostBase, PostOut, ReactionBase
from src.posts.service.db_operations import get_post_by_id, get_posts_by_user, create_post, update_post, delete_post, \
    create_reaction
from src.profile.models import UserIn


router = APIRouter(prefix="/post")


@router.get("/user/{username}", response_model=list[PostOut])
async def get_post_by_username(username: str):
    return await get_posts_by_user(username)


@router.get("/{post_id}", response_model=PostOut)
async def get_post_id(post_id: int):
    return await get_post_by_id(post_id)


@router.post("/user/create", response_model=PostOut)
async def create_new_post(post_data: PostBase, user: UserIn = Depends(get_current_user)):
    return await create_post(post_data, user.username)


@router.put("/update/{post_id}")
async def update_user_post(post_id: int, post_data: PostBase, user: UserIn = Depends(get_current_user)):
    return await update_post(post_id, post_data, user.username)


@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_post(post_id: int, user: UserIn = Depends(get_current_user)):
    return await delete_post(post_id, user.username)


@router.post("/reaction", status_code=status.HTTP_204_NO_CONTENT)
async def post_reaction(reaction_data: ReactionBase, user: UserIn = Depends(get_current_user)):
    return await create_reaction(reaction_data, user)
