from custom_node_helper import CustomNodeHelper


class ComfyUI_Essentials(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type("LoadCLIPSegModels"):
            weights_to_download.extend(["models--CIDAS--clipseg-rd64-refined"])
