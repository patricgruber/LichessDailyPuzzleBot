import os
import puzzle
from io import BytesIO

from nio import AsyncClient, UploadResponse

env_variables = [
    "MATRIX_HOMESERVER",
    "MATRIX_USER_ID",
    "MATRIX_ACCESS_TOKEN",
    "MATRIX_DEVICE_ID",
    "MATRIX_ROOM_ID"
]

any_not_set = False
for env_var in env_variables:
    if not os.environ.get(env_var):
        any_not_set = True
        print(f"Environment variable {env_var} is not set")

if any_not_set:
    exit(-1)

class Client:
    client: AsyncClient
    room_id: str

    def __init__(self):
        self.client = AsyncClient(os.environ.get("MATRIX_HOMESERVER"), os.environ.get("MATRIX_USER_ID"))
        self.client.access_token = os.environ.get("MATRIX_ACCESS_TOKEN")
        self.client.device_id = os.environ.get("MATRIX_DEVICE_ID")
        self.room_id = os.environ.get("MATRIX_ROOM_ID")

    async def send_solution(self, p: puzzle.Puzzle):
        solution_str = "\n".join(p.solution)
        content = {
            "body": f"Solution for Puzzle - {p.get_timestamp_str()}:\n{solution_str}",
            "msgtype": "m.text",
        }
        await self.client.room_send(self.room_id, message_type="m.room.message", content=content)

    async def send_board(self, p: puzzle.Puzzle):
        png_file = p.get_board_as_bytesio()
        file_size = len(png_file.getvalue())

        file = BytesIO(png_file.getvalue())

        resp, maybe_keys = await self.client.upload(
            file,
            content_type="image/png",
            filesize=file_size
        )
        if isinstance(resp, UploadResponse):
            print("Image was uploaded successfully to server. ")
        else:
            print(f"Failed to upload image. Failure response: {resp}")
            return

        await self.client.room_send(self.room_id, message_type="m.room.message", content={"body": f"Puzzle - {p.get_timestamp_str()}", "msgtype": "m.text"})

        content = {
            "body": f"Puzzle - {p.get_timestamp_str()}",
            "info": {
                "mimetype": "image/png",
                "w": 750,
                "h": 750,
            },
            "msgtype": "m.image",
            "url": resp.content_uri,
        }
        await self.client.room_send(self.room_id, message_type="m.room.message", content=content)

    async def close(self):
        await self.client.close()
