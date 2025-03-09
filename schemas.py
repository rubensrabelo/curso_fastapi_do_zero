from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserPublic(BaseModel):
    id: int | None = None
    username: str
    email: EmailStr


class UserSchema(UserPublic):
    password: str


class UserList(UserPublic):
    users: list[UserPublic]
