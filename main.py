from fastapi import FastAPI
from starlette import status

from schemas import Message

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
