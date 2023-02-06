import requests
import puzzle
import tempfile
import os


class Client:
    def __init__(self):
        self.session = requests.session()
        self.group_id = os.environ.get("GROUP_ID")
        if not self.group_id:
            raise Exception("Env variable GROUP_ID not set")
        self.url = "http://localhost:1234/api/v1/rpc"

    def send_solution(self, p: puzzle.Puzzle):
        solution_str = p.get_nice_solution_str()
        message = f"Solution for Puzzle - {p.get_timestamp_str()}:\n{solution_str}"
        params = {
            "groupId": self.group_id,
            "message": message
        }
        r = self.session.post(self.url, json=_build_json_rpc_message("send", params))
        if r.status_code not in [200, 201]:
            raise Exception(f"Error when sending the puzzle solution: ({r.status_code})\n{r.content}")

    def send_board(self, p: puzzle.Puzzle):
        temp_image_file = tempfile.mktemp()
        with open(temp_image_file, "wb") as f:
            f.write(p.get_board_as_bytesio().getvalue())

        puzzle_title = f"Puzzle - {p.get_timestamp_str()}"
        params = {
            "groupId": self.group_id,
            "message": puzzle_title,
            "attachment": temp_image_file
        }
        r = self.session.post(self.url, json=_build_json_rpc_message("send", params))

        os.remove(temp_image_file)

        if r.status_code not in [200, 201]:
            raise Exception(f"Error when sending the puzzle title: ({r.status_code})\n{r.content}")


def _build_json_rpc_message(method, params):
    json_rpc_message = {
        "jsonrpc": "2.0",
        "method": method
    }

    if params:
        json_rpc_message["params"] = params
    return json_rpc_message