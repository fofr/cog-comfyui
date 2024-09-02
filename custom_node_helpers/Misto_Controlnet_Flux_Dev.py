from custom_node_helper import CustomNodeHelper

CONTROLNETS = [
    "mistoline_flux.dev_v1.safetensors",
]

class Misto_Controlnet_Flux_Dev(CustomNodeHelper):
    @staticmethod
    def models():
        return CONTROLNETS

    @staticmethod
    def weights_map(base_url):
        controlnet_map = {
            model: {
                "url": f"{base_url}/controlnet/{model}.tar",
                "dest": "ComfyUI/models/TheMisto_model/",
            }
            for model in CONTROLNETS
        }
        return controlnet_map
