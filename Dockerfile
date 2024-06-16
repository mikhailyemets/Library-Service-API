FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHOUNNBUFFERED 1
ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR app/

COPY . .
RUN pip install -r requirements.txt
