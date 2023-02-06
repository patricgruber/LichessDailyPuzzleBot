#!/usr/bin/env python3

import datetime

import dateutil.relativedelta

import puzzle
import signal
import database


def main():
    client = signal.Client()

    print("Checking if database is initialized... ", end="")
    if not database.is_initialized():
        print("Not initialized")
        print("Initializing... ", end="")
        database.initialize()
    print("Initialized")

    yesterday = datetime.date.today() - dateutil.relativedelta.relativedelta(days=1)
    print(f"Receiving puzzle for date {yesterday} from database... ", end="")
    old_puzzle = database.retrieve_puzzle(yesterday)
    if old_puzzle:
        print("Found")
        print("Sending solution for yesterday's puzzle... ", end="")
        client.send_solution(old_puzzle)
        print("Ok")
    else:
        print("Not found")

    print("Fetching today's puzzle... ", end="")
    new_puzzle = puzzle.get_daily_puzzle()
    print("Ok")

    print("Storing today's puzzle in the database... ", end="")
    database.store_puzzle(new_puzzle)
    print("Ok")

    print("Sending board to group... ", end="")
    client.send_board(new_puzzle)
    print("Ok")


if __name__ == "__main__":
    main()
