from custom_node_helper import CustomNodeHelper

MODELS = [
    "face_yolov8n.pt",
    "appearance_feature_extractor.safetensors",
    "motion_extractor.safetensors",
    "spade_generator.safetensors",
    "stitching_retargeting_module.safetensors",
    "warping_module.safetensors",
]


class ComfyUI_Advanced_Live_Portrait(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type_in(["ExpressionEditor", "AdvancedLivePortrait"]):
            weights_to_download.extend(MODELS)
