FROM python:3.11

RUN mkdir -p /usr/src/
WORKDIR /usr/src/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY requirements.txt /usr/src/

RUN pip install -r requirements.txt

COPY . /usr/src/
