import datetime
import sqlite3
import pickle
from puzzle import Puzzle


connection = sqlite3.connect("/app/data/puzzle.db")


def is_initialized():
    cur = connection.cursor()
    result = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='puzzle'")
    return result.fetchone() is not None


def initialize():
    cur = connection.cursor()
    cur.execute("CREATE TABLE puzzle (publish_date, serialized)")
    connection.commit()


def store_puzzle(puzzle: Puzzle):
    cur = connection.cursor()
    serialized = pickle.dumps(puzzle)
    cur.execute("INSERT INTO puzzle (publish_date, serialized) VALUES (?, ?)", (puzzle.timestamp.date(), serialized))
    connection.commit()


def retrieve_puzzle(date: datetime.date):
    cur = connection.cursor()
    result = cur.execute("SELECT serialized FROM puzzle WHERE publish_date=?", (date,))
    row = result.fetchone()

    if row is None:
        return None

    return pickle.loads(row[0])
