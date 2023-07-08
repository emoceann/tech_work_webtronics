from src.settings import get_settings

settings = get_settings()


TORTOISE_ORM = {
    "connections": {
        "default": f"asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@db/{settings.POSTGRES_DB}"
    },
    "apps": {
        "models": {
            "models": ["src.profile.dao", "src.posts.dao", "aerich.models"],
            "default_connection": "default",
        },
    },
}
