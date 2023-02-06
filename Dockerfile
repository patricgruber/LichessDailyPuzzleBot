FROM debian:11

ARG VERSION=0.11.6
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /temp
RUN apt -y update && apt -y install python3 python3-pip cron wget openjdk-17-jre imagemagick

RUN wget https://github.com/AsamK/signal-cli/releases/download/v$VERSION/signal-cli-$VERSION-Linux.tar.gz && \
	tar xf signal-cli-$VERSION-Linux.tar.gz -C /opt && \
	ln -sf /opt/signal-cli-$VERSION/bin/signal-cli /usr/local/bin/

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY *.py ./
RUN chmod +x bot.py

COPY docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

RUN echo '0 8 * * * /app/bot.py' > crontab.txt && \
    crontab crontab.txt

CMD './docker-entrypoint.sh'