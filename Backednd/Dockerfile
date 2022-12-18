FROM python:3.9

WORKDIR /app

COPY ./requierments.txt .

COPY ./API ./API

COPY ./DB ./DB

RUN pip install --no-cache-dir --upgrade -r ./requierments.txt

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y


CMD ["uvicorn", "API.main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]