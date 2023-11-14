FROM python:3.10-slim-buster

WORKDIR /fapi

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY .env .env

EXPOSE 5328

ENV FLASK_APP = index.py
ENV S3_ENDPOINT=http://s3-service:9000/s3

CMD ["python3", "index.py"]