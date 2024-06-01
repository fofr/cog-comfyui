from custom_node_helper import CustomNodeHelper

class ComfyUI_KJNodes(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type_in(["BatchCLIPSeg", "DownloadAndLoadCLIPSeg"]):
            weights_to_download.extend(["models--CIDAS--clipseg-rd64-refined"])

    @staticmethod
    def check_for_unsupported_nodes(node):
        unsupported_nodes = {
            "StabilityAPI_SD3": "Calling an external API and passing your key is not supported and is unsafe",
            "Superprompt": "Superprompt is not supported as it needs to download T5 weights",
        }
        node.raise_if_unsupported(unsupported_nodes)
