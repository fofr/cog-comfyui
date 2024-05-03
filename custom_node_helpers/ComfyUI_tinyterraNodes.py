from custom_node_helper import CustomNodeHelper


class ComfyUI_tinyterraNodes(CustomNodeHelper):
    @staticmethod
    def check_for_unsupported_nodes(node):
        if node.is_type("ttN imageREMBG"):
            raise ValueError(
                "imageREMBG node is not supported in tinyterraNodes. Recommend using RemBGSession from ComfyUI_Essentials"
            )
