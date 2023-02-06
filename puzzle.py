import requests
import chess
import chess.svg
from io import BytesIO
from typing import List, Optional
import os
import datetime
import pickle


class Puzzle:
    id: str
    pgn: str
    solution: List[str]
    timestamp: datetime.datetime
    white_to_move: bool

    def __init__(self, id: str, pgn: str, solution: List[str], timestamp: datetime.datetime):
        self.id = id
        self.pgn = pgn
        self.white_to_move = len(self.pgn.split(" ")) % 2 == 0
        self.solution = []

        board = self._get_board()
        for san_move in solution:
            move = board.parse_san(san_move)
            self.solution.append(board.san(move))
            board.push_san(san_move)

        self.timestamp = timestamp

    def _get_board(self):
        board = chess.Board()
        for move in self.pgn.split(" "):
            board.push_san(move)
        return board

    def _get_board_as_svg(self):
        board = self._get_board()
        return chess.svg.board(board, flipped=not self.white_to_move, lastmove=board.peek(), colors={"square light": "#f0d9b5", "square dark": "#b58863"}, coordinates=False)

    def get_board_as_bytesio(self) -> BytesIO:
        with open("board.svg", "w") as f:
            f.write(self._get_board_as_svg())
        os.system("convert -density 500 -resize 750x750 board.svg board.png")

        png_file = BytesIO()
        with open("board.png", "rb") as f:
            png_file.write(f.read())

        os.system("rm board.png board.svg")
        return png_file

    def get_timestamp_str(self) -> str:
        return self.timestamp.strftime("%d.%m.%Y")

    def get_nice_solution_str(self) -> str:
        moves = self.solution.copy()
        if not self.white_to_move:
            moves = ["..."] + moves

        output = ""
        for i in range(len(moves)):
            if i % 2 == 0:
                if i > 0:
                    output += "\n"
                output += f"{i//2+1}: "
            output += f"{moves[i]} "
        return output


def get_daily_puzzle() -> Optional[Puzzle]:
    res = requests.get("https://lichess.org/api/puzzle/daily")
    if res.status_code != 200:
        print(f"[ERROR] {res.status_code} - {res.content}")

    json = res.json()

    return Puzzle(json["puzzle"]["id"], json["game"]["pgn"], json["puzzle"]["solution"], datetime.datetime.now())
