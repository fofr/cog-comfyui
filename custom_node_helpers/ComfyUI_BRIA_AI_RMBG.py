from custom_node_helper import CustomNodeHelper
from node import Node

MODELS = [
    "RMBG-1.4/model.pth",
]

class ComfyUI_BRIA_AI_RMBG(CustomNodeHelper):
    @staticmethod
    def models():
        return MODELS

    @staticmethod
    def add_weights(weights_to_download, node):
        if Node.is_type(node, "BRIA_RMBG_ModelLoader_Zho"):
            weights_to_download.extend(MODELS)

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/custom_nodes/ComfyUI-BRIA_AI-RMBG/{model}.tar",
                "dest": "ComfyUI/custom_nodes/ComfyUI-BRIA_AI-RMBG/",
            }
            for model in MODELS
        }
