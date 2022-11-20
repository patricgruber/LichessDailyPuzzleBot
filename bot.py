#!/usr/bin/env python3

import asyncio
import datetime

import dateutil.relativedelta

import puzzle
import matrix
import database


async def main():
    client = matrix.Client()

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
        await client.send_solution(old_puzzle)
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
    await client.send_board(new_puzzle)
    print("Ok")

    await client.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
