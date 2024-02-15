class ComfyUI_InstantID:
    @staticmethod
    def add_weights(weights_to_download, node):
        if "class_type" in node and node["class_type"] in [
            "InstantIDFaceAnalysis",
        ]:
            weights_to_download.append("antelopev2")
