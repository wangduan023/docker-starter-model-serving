FROM paddlepaddle/paddle:1.5.1

LABEL maintainer "345keji <wangduan023@gmail.com>"

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]
