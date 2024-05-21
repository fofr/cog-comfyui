from custom_node_helper import CustomNodeHelper

MODELS = ["MTEED.pth"]


class ComfyUI_Anyline(CustomNodeHelper):
    @staticmethod
    def models():
        return MODELS

    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type("AnyLinePreprocessor"):
            weights_to_download.extend(MODELS)

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/custom_nodes/ComfyUI-Anyline/checkpoints/Anyline/{model}.tar",
                "dest": "ComfyUI/custom_nodes/ComfyUI-Anyline/checkpoints/Anyline",
            }
            for model in MODELS
        }
