FROM python:3.8-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./server.py ./server.py
COPY ./sync_transactions.py ./sync_transactions.py

CMD [ "python3", "server.py" ]