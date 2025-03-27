from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette import status

from database import get_session
from models import User
from schemas import Message, UserPublic, UserSchema, UserList
from security import get_password_hash, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
        "/",
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

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=UserList
)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {
        "users": users
    }


@router.get(
        "/{user_id}",
        status_code=status.HTTP_200_OK,
        response_model=UserPublic
)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    return db_user


@router.put(
        "/{user_id}",
        status_code=status.HTTP_200_OK,
        response_model=UserPublic
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions'
        )
    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email

        session.commit()
        session.refresh(current_user)
        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or Email already exists"
        )


@router.delete(
        "/{user_id}",
        response_model=Message,
)
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough permissions'
        )
    session.delete(current_user)
    session.commit()
    return {
        "message": "User deleted"
    }
