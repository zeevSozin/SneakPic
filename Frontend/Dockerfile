FROM python:3.9

WORKDIR /Frontend

COPY ./requierments.txt .

COPY ./app ./app

COPY ./config.ini .

RUN pip install --no-cache-dir --upgrade -r ./requierments.txt

RUN apt-get update

CMD ["streamlit","run" , "app/main.py", "--server.address", "0.0.0.0", "--server.port", "8081"]