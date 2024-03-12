MODELS = [
    "rife47.pth",
]


class ComfyUI_Frame_Interpolation:
    @staticmethod
    def models():
        return MODELS

    @staticmethod
    def add_weights(weights_to_download, node):
        if "class_type" in node and node["class_type"] in [
            "RIFE VFI",
        ]:
            weights_to_download.extend(MODELS)

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife/{model}.tar",
                "dest": "ComfyUI/custom_nodes/ComfyUI-Frame-Interpolation/ckpts/rife",
            }
            for model in MODELS
        }
