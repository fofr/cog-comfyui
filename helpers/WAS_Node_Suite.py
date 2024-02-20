CLIPSEG_MODELS = [
    "models--CIDAS--clipseg-rd64-refined",
]


class WAS_Node_Suite:
    @staticmethod
    def models():
        return CLIPSEG_MODELS

    @staticmethod
    def add_weights(weights_to_download, node):
        node_class = node.get("class_type")
        model_name = node.get("inputs", {}).get("model")
        if (
            node_class == "CLIPSeg Model Loader"
            and model_name == "CIDAS/clipseg-rd64-refined"
        ):
            weights_to_download.extend(CLIPSEG_MODELS)

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/clipseg/{model}.tar",
                "dest": "ComfyUI/models/clipseg",
            }
            for model in CLIPSEG_MODELS
        }

    @staticmethod
    def check_for_unsupported_nodes(node):
        unsupported_nodes = {
            "BLIP Model Loader": "BLIP version 1 not supported by Transformers",
            "BLIP Analyze Image": "BLIP version 1 not supported by Transformers",
            "CLIPTextEncode (NSP)": "Makes an HTTP request out to a Github file",
            "Diffusers Model Loader": "Diffusers is not going to be included as a requirement for this custom node",
            "Diffusers Hub Model Down-Loader": "Diffusers is not going to be included as a requirement for this custom node",
            "SAM Model Loader": "There are better SAM Loader modules to use. This implementation is not supported",
            "Text Parse Noodle Soup Prompts": "Makes an HTTP request out to a Github file",
            "Text Random Prompt": "Makes an HTTP request out to Lexica, which is unsupported",
            "True Random.org Number Generator": "Needs an API key which cannot be supplied",
            "Image Seamless Texture": "img2texture dependency has not been added",
            "Image Rembg (Remove Background)": "rembg dependency has not been added because it causes custom nodes to fail",
            "MiDaS Model Loader": "WAS MiDaS nodes are not currently supported",
            "MiDaS Mask Image": "WAS MiDaS nodes are not currently supported",
            "MiDaS Depth Approximation": "WAS MiDaS nodes are not currently supported",
            "Text File History Loader": "History is not persisted",
        }
        node_class = node.get("class_type")
        if node_class in unsupported_nodes:
            reason = unsupported_nodes[node_class]
            raise ValueError(f"{node_class} node is not supported: {reason}")
