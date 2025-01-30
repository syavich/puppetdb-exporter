FROM ubuntu:latest
MAINTAINER Sergey Yavich

ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"
RUN apt-get update && apt-get install -y python2.7 python-pip
COPY app /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 8000
ENTRYPOINT ["python", "app.py"]
