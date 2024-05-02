from custom_node_helper import CustomNodeHelper
from node import Node

BASE_PATH = "/root/.u2net/"
MODELS = [
    "isnet-anime.onnx",
    "isnet-general-use.onnx",
    "silueta.onnx",
    "u2net.onnx",
    "u2net_cloth_seg.onnx",
    "u2net_human_seg.onnx",
    "u2netp.onnx",
    "vit_b-decoder-quant.onnx",
    "vit_b-encoder-quant.onnx",
]


class rembg(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        # RemBGSession+ is in ComfyUI_essentials
        if Node.is_type(node, "RemBGSession+"):
            model = Node.value(node, "model")
            model_weights = {
                "u2net: general purpose": ["u2net.onnx"],
                "u2netp: lightweight general purpose": ["u2netp.onnx"],
                "u2net_human_seg: human segmentation": ["u2net_human_seg.onnx"],
                "u2net_cloth_seg: cloths": ["u2net_cloth_seg.onnx"],
                "silueta: very small u2net": ["silueta.onnx"],
                "isnet-general-use: general purpose": ["isnet-general-use.onnx"],
                "isnet-anime: anime illustrations": ["isnet-anime.onnx"],
                "sam: general purpose": [
                    "vit_b-decoder-quant.onnx",
                    "vit_b-encoder-quant.onnx",
                ],
            }
            if model in model_weights:
                weights_to_download.extend(model_weights[model])

        # Image Rembg (Remove Background) is in WAS nodes
        elif Node.is_type(node, "Image Rembg (Remove Background)"):
            model = Node.value(node, "model")
            if model == "sam":
                weights_to_download.extend(
                    [
                        "vit_b-decoder-quant.onnx",
                        "vit_b-encoder-quant.onnx",
                    ]
                )
            else:
                weights_to_download.extend([f"{model}.onnx"])

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/rembg/{model}.tar",
                "dest": f"{BASE_PATH}{model}",
            }
            for model in MODELS
        }
