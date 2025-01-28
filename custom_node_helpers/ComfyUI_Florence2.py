import os
from custom_node_helper import CustomNodeHelper


class ComfyUI_Florence2(CustomNodeHelper):
    @staticmethod
    def prepare(**kwargs):
        # create the LLM folder in ComfyUI/models/LLM to avoid warnings
        if not os.path.exists("ComfyUI/models/LLM"):
            os.makedirs("ComfyUI/models/LLM")
