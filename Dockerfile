FROM python:3.7.4-buster

LABEL maintainer "345keji <wangduan023@gmail.com>"

ENV HTTP_URL="http://www.github.com"

COPY requirements.txt .

RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
#RUN pip install --upgrade -r requirements.txt
COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["sh", "-c","python app/server.py serve ${HTTP_URL}"]
