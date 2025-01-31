FROM python:3.9

WORKDIR /app

ARG CHUNK_ID

ENV CHUNK_ID=${CHUNK_ID}

COPY requirements.txt .

COPY app.py .

RUN pip install -r requirements.txt

CMD python3 app.py 


