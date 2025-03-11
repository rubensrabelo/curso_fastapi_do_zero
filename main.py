from fastapi import FastAPI, HTTPException
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


@app.put(
        "/users/{user_id}",
        status_code=status.HTTP_200_OK,
        response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user_with_id = UserSchema(**user.model_dump())
    user_with_id.id = user_id
    database[user_id - 1] = user_with_id
    return user_with_id
