FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get upgrade -y

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["--host", "0.0.0.0", "--port", "8001"]

ENTRYPOINT ["uvicorn", "server:app", "--port", "8001"]