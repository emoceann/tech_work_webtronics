from fastapi import FastAPI
from tortoise import Tortoise

from src.db.config import TORTOISE_ORM
from src.profile.api import router as profile_router
from src.auth.api import router as auth_router
from src.posts.api import router as post_router

app = FastAPI()
app.include_router(profile_router)
app.include_router(auth_router)
app.include_router(post_router)


@app.on_event("startup")
async def init_db():
    await Tortoise.init(
        config=TORTOISE_ORM
    )


@app.on_event("shutdown")
async def close_db():
    await Tortoise.close_connections()
