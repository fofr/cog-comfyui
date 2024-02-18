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
        unsupported_nodes = [
            "BLIP Model Loader",
            "Diffusers Model Loader",
            "Diffusers Hub Model Down-Loader",
        ]
        node_class = node.get("class_type")
        if node_class in unsupported_nodes:
            raise ValueError(f"{node_class} nodes are not supported.")
