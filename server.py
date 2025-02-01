from fastapi import FastAPI
from typing import Optional

# FastAPI 인스턴스 생성
app = FastAPI()


# GET 요청을 처리하는 엔드포인트
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI example!"}
