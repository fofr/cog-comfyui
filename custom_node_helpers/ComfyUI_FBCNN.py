from custom_node_helper import CustomNodeHelper

class ComfyUI_FBCNN(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type("JPEG artifacts removal FBCNN"):
            weights_to_download.append("fbcnn_color.pth")
