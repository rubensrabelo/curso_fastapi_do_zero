from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserPublic(BaseModel):
    id: int | None = None
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserSchema(UserPublic):
    password: str


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100
