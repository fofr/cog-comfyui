import os
import shutil
from typing import List
from cog import BasePredictor, Input, Path
from comfyui_helpers import ComfyUIHelpers

OUTPUT_DIR = "/tmp/outputs"
INPUT_DIR = "/tmp/inputs"
COMFYUI_TEMP_OUTPUT_DIR = "ComfyUI/temp"

with open("examples/sdxlturbo_example.json", "r") as file:
    EXAMPLE_WORKFLOW_JSON = file.read()


class Predictor(BasePredictor):
    def setup(self):
        self.comfyUI = ComfyUIHelpers("127.0.0.1:8188")
        self.comfyUI.start_server(OUTPUT_DIR)

    def predict(
        self,
        workflow_json: str = Input(description="JSON workflow", default=""),
        return_temp_files: bool = Input(
            description="Return temp files, such as preprocessed controlnet images. Useful for debugging.",
            default=False,
        ),
    ) -> List[Path]:
        """Run a single prediction on the model"""
        for directory in [OUTPUT_DIR, INPUT_DIR, COMFYUI_TEMP_OUTPUT_DIR]:
            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)

        # TODO: Record the previous models loaded
        # If different, run /free to free up models and memory

        wf = self.comfyUI.load_workflow(workflow_json or EXAMPLE_WORKFLOW_JSON)
        self.comfyUI.connect()
        self.comfyUI.run_workflow(wf)

        # Log the contents of the temp and output directories recursively
        def log_and_collect_files(directory, prefix=""):
            files = []
            for f in os.listdir(directory):
                path = os.path.join(directory, f)
                if os.path.isfile(path):
                    print(f"{prefix}{f}")
                    files.append(Path(path))
                elif os.path.isdir(path):
                    print(f"{prefix}{f}/")
                    files.extend(log_and_collect_files(path, prefix=f"{prefix}{f}/"))
            return files

        files = []
        output_directories = [OUTPUT_DIR]
        if return_temp_files:
            output_directories.append(COMFYUI_TEMP_OUTPUT_DIR)

        for directory in output_directories:
            print(f"Contents of {directory}:")
            files.extend(log_and_collect_files(directory))

        return files
