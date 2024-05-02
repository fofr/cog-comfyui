class ComfyUI_Reactor_Node:
    facedetection_weights = {
        "retinaface_resnet50": "detection_Resnet50_Final.pth",
        "retinaface_mobile0.25": "detection_mobilenet0.25_Final.pth",
        "YOLOv5l": "yolov5l-face.pth",
        "YOLOv5n": "yolov5n-face.pth",
    }

    @staticmethod
    def add_weights(weights_to_download, node):
        if "class_type" in node and node["class_type"] in [
            "ReActorFaceSwap",
            "ReActorLoadFaceModel",
            "ReActorSaveFaceModel",
        ]:
            weights_to_download.append("models/buffalo_l")
            weights_to_download.append("parsing_parsenet.pth")

            if "facedetection" in node["inputs"]:
                facedetection_model = node["inputs"]["facedetection"]
                if facedetection_model in ComfyUI_Reactor_Node.facedetection_weights:
                    weights_to_download.append(
                        ComfyUI_Reactor_Node.facedetection_weights[facedetection_model]
                    )
