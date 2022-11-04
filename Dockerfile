FROM python:3.10-alpine

RUN apk add g++ imagemagick

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY *.py ./
RUN chmod +x bot.py

RUN echo '0 8 * * * /app/bot.py' > crontab.txt

RUN crontab crontab.txt

ENTRYPOINT ["/usr/sbin/crond", "-f", "-l", "8"]