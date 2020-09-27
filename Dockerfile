FROM python:3.7.4

COPY ./deploy/sources.list /etc/apt/sources.list

RUN apt-get update && apt-get install -y vim && apt-get install -y p7zip-full

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . .

CMD gunicorn manage:app -c deploy/gunicorn_conf.py
