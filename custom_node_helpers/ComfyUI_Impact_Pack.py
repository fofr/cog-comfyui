from custom_node_helper import CustomNodeHelper

class ComfyUI_Impact_Pack(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        if "class_type" in node and node["class_type"] in [
            "UltralyticsDetectorProvider",
        ]:
            weights_to_download.extend([
                "bbox/hand_yolov8s.pt",
                "bbox/face_yolov8m.pt",
                "segm/person_yolov8m-seg.pt"
            ])
