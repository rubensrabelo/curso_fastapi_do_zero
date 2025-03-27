from fastapi import FastAPI
from starlette import status

from routers import auth, users
from schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)


@app.get(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=Message
        )
def read_root():
    return {
        "message": "Hello, world!"
    }
