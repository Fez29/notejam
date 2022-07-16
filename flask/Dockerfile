FROM python:2.7

#ADD ./.aws /root/.aws

COPY ./requirements.txt .

RUN pip install -r ./requirements.txt

COPY . .

ENV DEBUG=false

CMD [ "python", "./runserver.py" ]