CONTROLNET_AUX_MODELS = {
    "dw-ll_ucoco_384.onnx": "yzd-v/DWPose",
    "yolox_l.onnx": "yzd-v/DWPose",
    "ZoeD_M12_N.pt": "lllyasviel/Annotators",
}


class ComfyUI_Controlnet_Aux:
    # Controlnet preprocessor models are not included in the API JSON
    # We need to add them manually based on the nodes being used to
    # avoid them being downloaded automatically from elsewhere

    @staticmethod
    def weights_mapping():
        return {"Zoe-DepthMapPreprocessor": "ZoeD_M12_N.pt"}

    @staticmethod
    def weights_map(base_url):
        return {
            key: {
                "url": f"{base_url}/custom_nodes/comfyui_controlnet_aux/{key}.tar",
                "dest": f"ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts/{CONTROLNET_AUX_MODELS[key]}",
            }
            for key in CONTROLNET_AUX_MODELS
        }

    @staticmethod
    def add_controlnet_preprocessor_weight(weights_to_download, node):
        if (
            "class_type" in node
            and node["class_type"] in ComfyUI_Controlnet_Aux.weights_mapping()
        ):
            weights_to_download.append(
                ComfyUI_Controlnet_Aux.weights_mapping()[node["class_type"]]
            )
