FROM python:3.9

WORKDIR /app

ARG CITY_NAME

ARG PROVINCE_CODE

ARG CHUNK_NO

ENV CITY_NAME=${CITY_NAME}

ENV PROVINCE_CODE=${PROVINCE_CODE}

ENV CITY_NAME=${CHUNK_NO}

COPY requirements.txt .


COPY app.py .

RUN pip install -r requirements.txt

CMD python3 app.py 


