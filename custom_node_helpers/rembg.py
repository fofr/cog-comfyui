from custom_node_helper import CustomNodeHelper


class rembg(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        # RemBGSession+ is in ComfyUI_essentials
        if node.is_type("RemBGSession+"):
            model = node.input("model")
            model_weights = {
                "u2net: general purpose": ["u2net.onnx"],
                "u2netp: lightweight general purpose": ["u2netp.onnx"],
                "u2net_human_seg: human segmentation": ["u2net_human_seg.onnx"],
                "u2net_cloth_seg: cloths Parsing": ["u2net_cloth_seg.onnx"],
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
        elif node.is_type("Image Rembg (Remove Background)"):
            model = node.input("model")
            if model == "sam":
                weights_to_download.extend(
                    [
                        "vit_b-decoder-quant.onnx",
                        "vit_b-encoder-quant.onnx",
                    ]
                )
            else:
                weights_to_download.extend([f"{model}.onnx"])
