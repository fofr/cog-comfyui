class ComfyUI_Controlnet_Aux:
    # Controlnet preprocessor models are not included in the API JSON
    # We need to add them manually based on the nodes being used to
    # avoid them being downloaded automatically from elsewhere
    @staticmethod
    def weights_mapping():
        return {"Zoe-DepthMapPreprocessor": "ZoeD_M12_N.pt"}

    @staticmethod
    def add_controlnet_preprocessor_weight(weights_to_download, node):
        if (
            "class_type" in node
            and node["class_type"] in ComfyUI_Controlnet_Aux.weights_mapping()
        ):
            weights_to_download.append(
                ComfyUI_Controlnet_Aux.weights_mapping()[node["class_type"]]
            )
