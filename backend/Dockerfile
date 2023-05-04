FROM python:3.11

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get -qq update

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

EXPOSE 8000