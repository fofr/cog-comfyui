class ComfyUI_KJNodes:
    @staticmethod
    def add_weights(weights_to_download, node):
        if node.get("class_type") == "BatchCLIPSeg":
            weights_to_download.extend(["models--CIDAS--clipseg-rd64-refined"])

    @staticmethod
    def check_for_unsupported_nodes(node):
        unsupported_nodes = {
            "StabilityAPI_SD3": "Calling an external API and passing your key is not supported and is unsafe",
            "Superprompt": "Superprompt is not supported as it needs to download T5 weights",
        }
        node_class = node.get("class_type")
        if node_class in unsupported_nodes:
            reason = unsupported_nodes[node_class]
            raise ValueError(f"{node_class} node is not supported: {reason}")
