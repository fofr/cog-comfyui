from custom_node_helper import CustomNodeHelper


class WAS_Node_Suite(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        if (
            node.is_type("CLIPSeg Model Loader")
            and node.input("model") == "CIDAS/clipseg-rd64-refined"
        ):
            weights_to_download.extend(["models--CIDAS--clipseg-rd64-refined"])

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
            "MiDaS Model Loader": "WAS MiDaS nodes are not currently supported",
            "MiDaS Mask Image": "WAS MiDaS nodes are not currently supported",
            "MiDaS Depth Approximation": "WAS MiDaS nodes are not currently supported",
            "Text File History Loader": "History is not persisted",
        }
        node.raise_if_unsupported(unsupported_nodes)
