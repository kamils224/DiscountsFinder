FROM python:3.8.1-slim-buster

WORKDIR /discounts_finder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY requirements.txt /discounts_finder/requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONPATH="$PYTHONPATH:/"

COPY . /discounts_finder