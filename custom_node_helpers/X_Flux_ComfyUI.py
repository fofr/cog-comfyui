from custom_node_helper import CustomNodeHelper

IPADAPTERS = [
    "flux-ip-adapter.safetensors",
]


class X_Flux_ComfyUI(CustomNodeHelper):
    @staticmethod
    def models():
        return IPADAPTERS

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/xlabs/ipadapter/{model}.tar",
                "dest": "ComfyUI/xlabs/ipadapter/",
            }
            for model in IPADAPTERS
        }
