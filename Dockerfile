FROM python:3.7
RUN apt-get update && apt-get -y install bash postgresql-common
WORKDIR /app

EXPOSE 9000

ADD requirements.txt .

RUN pip install -r requirements.txt

COPY . .


CMD [ "/bin/bash", "/app/run.sh" ]

