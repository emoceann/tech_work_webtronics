from pydantic import BaseModel, Field
from enum import Enum


class ReactionEnum(Enum):
    like = "like"
    dislike = "dislike"


class ReactionBase(BaseModel):
    post_id: int
    reaction_type: ReactionEnum

    class Config:
        use_enum_values = True


class PostBase(BaseModel):
    text: str


class PostOut(PostBase):
    id: int
    creator: str = Field(alias="creator_id")

    class Config:
        allow_populate_by_alias = True
        orm_mode = True
