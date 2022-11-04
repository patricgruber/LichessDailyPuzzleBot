# LichessDailyPuzzleMatrixBot
A dockerized solution to post the daily puzzle from lichess.org as an image to a Matrix room.

This python script runs in a Docker container and executes every day at 8 UTC.
The Matrix homeserver, credentials and room are configurable via env variables.

To start the project do the following:
1. Copy `.env.example` to `.env`
2. Change the env variables in `.env`
3. Start the docker container via `docker-compose up`
