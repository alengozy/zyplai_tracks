FROM python:3.11-slim-buster
    
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1


WORKDIR /
# install system dependencies
RUN apt-get update \
  && apt-get -y install libpq-dev gcc 

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .




