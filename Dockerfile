FROM python:3.10-slim-buster
WORKDIR /app

# Upgrade installed packages
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

