import requests
import json

url = 'http://127.0.0.1:8000/'

data = {"content": "서울을 100글자로 설명해줘"}

headers = {"Content-type": "application/json"}

# with requests.get(url+"stream?message=서울을100글자로설명해줘", data=json.dumps(data), headers=headers, stream=True) as r:
#     for chunk in r.iter_content(1024):
#         print(chunk.decode('utf-8'))
with requests.get(url+"stream", data=json.dumps(data), headers=headers, stream=True) as r:
    for chunk in r.iter_content(1024):
        print(chunk.decode('utf-8'))