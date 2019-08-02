FROM 3.7.4-buster

LABEL maintainer "345keji <wangduan023@gmail.com>"

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]
