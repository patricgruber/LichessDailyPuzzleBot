# LichessDailyPuzzleBot
A dockerized solution to post the daily puzzle from lichess.org as an image to a Signal group via ![signal-cli](https://github.com/AsamK/signal-cli)

This python script runs in a Docker container and executes every day at 8 UTC.
The Signal account and group id are configurable through environment variables in the `.env` file. 

To start the project do the following:
1. Copy `.env.example` to `.env`
2. Change the env variables in `.env`
3. Build the container with `docker-compose build`
4. Link your Signal account with `docker-compose run bot signal-cli link`
   1. This will show generate an URL like "sgnl://linkdevice?uuid=..."
   2. Generate a QR code out of that URL with the command `qrencode -o signal-link.png "<the URL>"`
   3. Open the generated image with an image viewer of your choice
   4. Link the server with your account via the Signal app on your phone by scanning the QR code
5. Start the container with `docker-compose up -d`
