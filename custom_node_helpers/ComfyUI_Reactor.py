from custom_node_helper import CustomNodeHelper


class ComfyUI_Reactor(CustomNodeHelper):
    facedetection_weights = {
        "retinaface_resnet50": "detection_Resnet50_Final.pth",
        "retinaface_mobile0.25": "detection_mobilenet0.25_Final.pth",
        "YOLOv5l": "yolov5l-face.pth",
        "YOLOv5n": "yolov5n-face.pth",
    }

    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type_in(
            [
                "ReActorFaceSwap",
                "ReActorLoadFaceModel",
                "ReActorSaveFaceModel",
                "ReActorFaceSwapOpt",
            ]
        ):
            weights_to_download.append("models/buffalo_l")
            weights_to_download.append("parsing_parsenet.pth")
            weights_to_download.append("vit-base-nsfw-detector")

            if node.has_input("facedetection"):
                facedetection_model = node.input("facedetection")
                if facedetection_model in ComfyUI_Reactor.facedetection_weights:
                    weights_to_download.append(
                        ComfyUI_Reactor.facedetection_weights[facedetection_model]
                    )
