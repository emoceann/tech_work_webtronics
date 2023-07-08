from fastapi import HTTPException
from starlette import status

from src.posts.dao import Post, Reaction
from src.posts.models import PostBase, ReactionBase
from src.profile.models import UserIn


async def get_post_by_id(post_id: int):
    return await Post.get_or_none(id=post_id)


async def filter_post_by_id_and_username(post_id: int, username: str):
    return await Post.filter(id=post_id, creator_id=username).first()


async def get_posts_by_user(username: str):
    posts = await Post.filter(creator_id=username)
    if not posts:
        return
    return posts


async def create_post(post_data: PostBase, username: str):
    return await Post.create(text=post_data.text, creator_id=username)


async def update_post(post_id: int, post_data: PostBase, username: str):
    post = await filter_post_by_id_and_username(post_id, username)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    post.text = post_data.text
    await post.save()
    return post


async def delete_post(post_id: int, username: str):
    post = await filter_post_by_id_and_username(post_id, username)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )
    await post.delete()


async def check_reaction_exists(post_id: int, username: str):
    return await Reaction.filter(post=post_id, user_id=username).exists()


async def create_reaction(reaction_data: ReactionBase, user: UserIn):
    post = await filter_post_by_id_and_username(reaction_data.post_id, user.username)
    if post:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can not react on your own post",
        )
    if await check_reaction_exists(reaction_data.post_id, user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already reacted",
        )
    await Reaction.create(post_id=reaction_data.post_id, reaction_type=reaction_data.reaction_type, user_id=user.username)
