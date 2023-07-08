from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(256) NOT NULL UNIQUE,
    "password" VARCHAR(256) NOT NULL,
    "email" VARCHAR(128) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "post" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "text" VARCHAR(2048) NOT NULL,
    "creator_id" VARCHAR(256) NOT NULL REFERENCES "user" ("username") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "reaction" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "reaction_type" VARCHAR(10) NOT NULL,
    "post_id" BIGINT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" VARCHAR(256) REFERENCES "user" ("username") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
