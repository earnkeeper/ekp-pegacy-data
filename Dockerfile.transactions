FROM python:3.8-buster

WORKDIR /app

COPY ./app/requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY ./app ./

CMD [ "python3", "main_transactions.py" ]