import requests


def googMoonExtract_info(data):
    contentid_mapping = {
        "12": "여행지",
        "14": "여행지",
        "15": "여행지",
        "25": "여행지",
        "28": "여행지",
        "32": "여행지",
        "38": "여행지",
        "39": "음식점",
    }

    extracted_data = []
    for item in data:
        info = {
            "카테고리": contentid_mapping[item.get("contenttypeid")],
            "장소명": item.get("title"),
            "주소": item.get("addr1"),
            "imgUrl": item.get("firstimage"),
        }
        extracted_data.append(info)
    return extracted_data


def googMoonGetData(keyword):
    googMoonParams = {
        "numOfRows": 20,
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "keyword": keyword,
        "_type": "json",
        "serviceKey": "1aTtm1FAPYi9yC9uklnKdMBUN6+4J1SlAMa4TbmxscnxFS0cZ51TaTL4d6rB4b2lrDMz/ovJjTVkrz+G1itnGg==",
    }
    GOOGMOONURL = "http://apis.data.go.kr/B551011/KorService1/searchKeyword1"
    response = requests.get(GOOGMOONURL, params=googMoonParams)
    if response.status_code != 200:
        return None
    data = response.json()
    if (
        ("response" not in data)
        or ("body" not in data["response"])
        or ("items" not in data["response"]["body"])
        or ("item" not in data["response"]["body"]["items"])
    ):
        return None
    result = googMoonExtract_info(data["response"]["body"]["items"]["item"])
    return result


def extract_first_word(location):
    if "_" in location:
        return location.split("_")[0]
    return location
