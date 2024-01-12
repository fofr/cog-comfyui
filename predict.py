import os
import shutil
from typing import List
from cog import BasePredictor, Input, Path
from comfyui_helpers import ComfyUIHelpers

OUTPUT_DIR = "/tmp/outputs"
INPUT_DIR = "/tmp/inputs"

with open("workflow_api_img2img.json", "r") as file:
    WORKFLOW_JSON = file.read()


class Predictor(BasePredictor):
    def setup(self):
        self.comfyUI = ComfyUIHelpers("127.0.0.1:8188")
        self.comfyUI.start_server(OUTPUT_DIR)

    def predict(
        self,
        workflow_json: str = Input(description="JSON workflow", default=False),
    ) -> List[Path]:
        """Run a single prediction on the model"""
        for directory in [OUTPUT_DIR, INPUT_DIR]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)

        wf = self.comfyUI.load_workflow(workflow_json or WORKFLOW_JSON)
        self.comfyUI.connect()
        self.comfyUI.run_workflow(wf)

        return [
            Path(os.path.join(OUTPUT_DIR, f))
            for f in os.listdir(OUTPUT_DIR)
            if os.path.isfile(os.path.join(OUTPUT_DIR, f))
        ]
