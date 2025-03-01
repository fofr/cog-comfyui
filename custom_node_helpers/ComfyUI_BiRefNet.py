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
        elif node.is_type("AutoDownloadBiRefNetModel"):
            model_name = node.input("model_name")
            weights_to_download.append(f"{model_name}.safetensors")
