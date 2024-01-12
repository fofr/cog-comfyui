import subprocess
import threading
import time
import json
import urllib
import uuid
import json
import websocket
from urllib.error import URLError


class ComfyUIHelpers:
    def __init__(self, server_address):
        self.server_address = server_address

    def start_server(self, output_directory):
        server_thread = threading.Thread(
            target=self.run_server, args=(output_directory,)
        )
        server_thread.start()

        while not self.is_server_running():
            time.sleep(1)  # Wait for 1 second before checking again

        print("Server running")

    def run_server(self, output_directory):
        command = f"python ./ComfyUI/main.py --output-directory {output_directory}"
        server_process = subprocess.Popen(command, shell=True)
        server_process.wait()

    def is_server_running(self):
        try:
            with urllib.request.urlopen(
                "http://{}/history/{}".format(self.server_address, "123")
            ) as response:
                return response.status == 200
        except URLError:
            return False

    def connect(self):
        self.client_id = str(uuid.uuid4())
        self.ws = websocket.WebSocket()
        self.ws.connect(
            "ws://{}/ws?clientId={}".format(self.server_address, self.client_id)
        )

    def queue_prompt(self, prompt):
        # Prompt is the loaded workflow (prompt is the label comfyUI uses)
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode("utf-8")
        req = urllib.request.Request(
            "http://{}/prompt".format(self.server_address), data=data
        )

        output = json.loads(urllib.request.urlopen(req).read())
        return output["prompt_id"]

    def wait_for_prompt_completion(self, prompt_id):
        while True:
            out = self.ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message["type"] == "executing":
                    data = message["data"]
                    if data["node"] is None and data["prompt_id"] == prompt_id:
                        break
            else:
                continue

    def load_workflow(self, workflow):
        return json.loads(workflow)

    def run_workflow(self, workflow_json):
        workflow = self.load_workflow(workflow_json)
        prompt_id = self.queue_prompt(workflow)
        self.wait_for_prompt_completion(prompt_id)
        output_json = self.get_history(prompt_id)
        print("outputs: ", output_json)

    def get_history(self, prompt_id):
        with urllib.request.urlopen(
            "http://{}/history/{}".format(self.server_address, prompt_id)
        ) as response:
            output = json.loads(response.read())
            return output[prompt_id]["outputs"]
