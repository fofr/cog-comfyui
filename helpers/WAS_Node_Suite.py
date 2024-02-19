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
        model_size = node.get("inputs", {}).get("model_size")
        if node_class == "CLIPSeg Model Loader" and model_name == "CIDAS/clipseg-rd64-refined":
            weights_to_download.extend(CLIPSEG_MODELS)
        elif node_class == "SAM Model Loader":
            sam_model_weights = {
                "ViT-H": "sam_vit_h_4b8939.pth",
                "ViT-B": "sam_vit_b_01ec64.pth",
                "ViT-L": "sam_vit_l_0b3195.pth",
            }
            if model_size in sam_model_weights:
                weights_to_download.append(sam_model_weights[model_size])

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
