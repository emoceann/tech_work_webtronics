from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str


class UserIn(UserBase):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
