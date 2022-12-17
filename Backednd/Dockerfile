FROM python:3.9

WORKDIR /app

COPY ./requierments.txt .

COPY ./API/main.py .

COPY ./DB .

COPY ./API/yolov5 ./yolov5



RUN pip install --no-cache-dir --upgrade -r ./requierments.txt

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y




CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]