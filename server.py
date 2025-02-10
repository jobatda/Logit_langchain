from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from fastapi.responses import StreamingResponse

from dotenv import load_dotenv

load_dotenv()
# FastAPI 인스턴스 생성

app = FastAPI()
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = llm | StrOutputParser()


@app.get("/invoke")
def sync_chat(message: str):
    response = chain.invoke(message)
    return response
