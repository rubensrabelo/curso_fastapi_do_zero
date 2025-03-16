from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from database import get_session
from models import User
from schemas import Message, UserPublic, UserSchema, UserList

app = FastAPI()


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
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already exists"
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists"
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
        "/users/",
        status_code=status.HTTP_200_OK,
        response_model=UserList
)
def read_users():
    return {
        "users": database
    }


@app.get(
        "/users/{user_id}",
        status_code=status.HTTP_200_OK,
        response_model=UserPublic
)
def read_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user_data = database[user_id - 1]
    return user_data


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


@app.delete(
        "/users/{user_id}",
        response_model=Message
)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    del database[user_id - 1]
    return {
        "message": "User deleted"
    }
