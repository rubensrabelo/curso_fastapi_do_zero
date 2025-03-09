from fastapi import FastAPI
from starlette import status

from schemas import Message, UserPublic, UserSchema, UserList

app = FastAPI()

database = []


@app.get(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=Message
        )
def read_root():
    return {
        "message": "Hello, world!"
    }


@app.post(
        "/users/",
        status_code=status.HTTP_201_CREATED,
        response_model=UserPublic
        )
def create_user(user: UserSchema):
    user_db = UserPublic(**user.model_dump())
    user_db.id = len(database) + 1
    database.append(user_db)
    return user_db


@app.get(
        "/users/",
        status_code=status.HTTP_200_OK,
        response_model=UserList
)
def read_users():
    return {
        "users": database
    }
