#!/usr/bin/env python3

import asyncio
import puzzle
import matrix

last_puzzle = None
current_puzzle = None


async def main():
    client = matrix.Client()

    old_puzzle = puzzle.Puzzle.from_disc()
    if old_puzzle:
        await client.send_solution(old_puzzle)

    new_puzzle = puzzle.get_daily_puzzle()
    await client.send_board(new_puzzle)

    new_puzzle.store_to_disc()
    await client.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run(main())
