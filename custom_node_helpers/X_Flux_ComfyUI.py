from custom_node_helper import CustomNodeHelper

IPADAPTERS = [
    "flux-ip-adapter.safetensors",
]

CONTROLNETS = [
    "flux-hed-controlnet-v3.safetensors",
    "flux-canny-controlnet-v3.safetensors",
    "flux-depth-controlnet-v3.safetensors",
]


class X_Flux_ComfyUI(CustomNodeHelper):
    @staticmethod
    def models():
        return IPADAPTERS + CONTROLNETS

    @staticmethod
    def weights_map(base_url):
        ipadapter_map = {
            model: {
                "url": f"{base_url}/xlabs/ipadapters/{model}.tar",
                "dest": "ComfyUI/models/xlabs/ipadapters/",
            }
            for model in IPADAPTERS
        }
        controlnet_map = {
            model: {
                "url": f"{base_url}/xlabs/controlnets/{model}.tar",
                "dest": "ComfyUI/models/xlabs/controlnets/",
            }
            for model in CONTROLNETS
        }
        return {**ipadapter_map, **controlnet_map}
