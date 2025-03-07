from fastapi import FastAPI
from starlette import status

from schemas import Message, UserPublic, UserSchema, UserDB

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
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=UserPublic
        )
def create_user(user: UserSchema):
    user_db = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_db)
    return user_db
