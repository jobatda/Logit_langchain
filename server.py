from fastapi import FastAPI
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from prompt import prompt
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from utils import googMoonGetData, googMoonExtract_info, extract_first_word
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credential=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)


class OutPut(BaseModel):
    카테고리: str = Field(description="장소에 대한 카테고리")
    장소명: str = Field(description="장소명 제공 데이터의")
    주소: str = Field(description="장소의 주소")


parser = JsonOutputParser(pydantic_object=OutPut)

prompt = prompt.partial(format_instructions=parser.get_format_instructions())

chain = prompt | model | parser


class TravelRequest(BaseModel):
    region: str  # 지역 이름
    duration: str  # 여행 기간 (일 단위)
    theme: List[str]  # 여행 테마 (예: ['adventure', 'relaxation'])


@app.post("/aiplanner")
async def create_travel_plan(request: TravelRequest):
    region = request.region
    duration = request.duration
    theme = request.theme

    question_format = "지역: {location}, 기간: {date}, 테마: {theme}"
    question = question_format.format(location=region, date=duration, theme=theme)

    apiInput = extract_first_word(region)
    if len(apiInput) > 2:
        apiInput = apiInput[:2]

    with_image = googMoonGetData(apiInput)

    if (with_image is None) or (len(with_image) == 0):
        return { "output": "" }  # 데이터 없으니깐 프론트에 데이터 없다고 알려줘야함

    filtered_data = []

    # data_without_imgUrl
    for item in with_image:
        spllitData = item["주소"].split(" ")
        if len(spllitData) > 1:
            if spllitData[1].startswith(apiInput):
                filtered_data.append(item)
        else:
            continue

    if filtered_data:
        return { "output": "" }
    #  filtered_data 검사 후 데이터 없으면 데이터 없다고 알려줘야함
    data_without_imgUrl = [
        {k: v for k, v in item.items() if k != "imgUrl"} for item in filtered_data
    ]

    # result = None

    if len(data_without_imgUrl) == 0:
        return { "output": "" }  # 추천할 데이터가 없다
    
    result = chain.invoke({"question": question, "context": data_without_imgUrl})

    place_to_imgUrl = {item["장소명"]: item["imgUrl"] for item in with_image}

    # result에 imgUrl 추가

    if "Day 1" in result:
        for item in result["Day 1"]:
            if (item["장소명"]) in place_to_imgUrl:
                data = place_to_imgUrl[item["장소명"]]
                if (data is not None) and (data != ""):
                    item["imgUrl"] = data
    if "Day 2" in result:
        for item in result["Day 2"]:
            if (item["장소명"]) in place_to_imgUrl:
                data = place_to_imgUrl[item["장소명"]]
                if (data is not None) and (data != ""):
                    item["imgUrl"] = data
    if "Day 3" in result:
        for item in result["Day 3"]:
            if (item["장소명"]) in place_to_imgUrl:
                data = place_to_imgUrl[item["장소명"]]
                if (data is not None) and (data != ""):
                    item["imgUrl"] = data
    return {
        "output": result,
    }
