from custom_node_helper import CustomNodeHelper

class ComfyUI_BrushNet(CustomNodeHelper):
    @staticmethod
    def check_for_unsupported_nodes(node):
        unsupported_nodes = {
            "Terminal": "Node is not supported",
        }
        node.raise_if_unsupported(unsupported_nodes)
