from custom_node_helper import CustomNodeHelper

MODELS = [
    "BiRefNet-DIS_ep580.pth",
    "BiRefNet-ep480.pth",
    "pvt_v2_b2.pth",
    "pvt_v2_b5.pth",
    "swin_base_patch4_window12_384_22kto1k.pth",
    "swin_large_patch4_window12_384_22kto1k.pth",
]

class ComfyUI_BiRefNet(CustomNodeHelper):
    @staticmethod
    def models():
        return MODELS

    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type("BiRefNet_ModelLoader_Zho"):
            weights_to_download.extend(MODELS)

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/BiRefNet/{model}.tar",
                "dest": "ComfyUI/models/BiRefNet/",
            }
            for model in MODELS
        }
