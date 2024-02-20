MODEL_WEIGHTS = {
    "sam_vit_h (2.56GB)": "sam_vit_h_4b8939.pth",
    "sam_vit_l (1.25GB)": "sam_vit_l_0b3195.pth",
    "sam_vit_b (375MB)": "sam_vit_b_01ec64.pth",
    "sam_hq_vit_h (2.57GB)": "sam_hq_vit_h.pth",
    "sam_hq_vit_l (1.25GB)": "sam_hq_vit_l.pth",
    "sam_hq_vit_b (379MB)": "sam_hq_vit_b.pth",
    "mobile_sam(39MB)": "mobile_sam.pt",
    "GroundingDINO_SwinT_OGC (694MB)": "groundingdino_swint_ogc.pth",
    "GroundingDINO_SwinB (938MB)": "groundingdino_swinb_cogcoor.pth",
}


class ComfyUI_Segment_Anything:
    @staticmethod
    def add_weights(weights_to_download, node):
        if "class_type" in node and node["class_type"] in [
            "SAMModelLoader (segment anything)",
            "GroundingDinoModelLoader (segment anything)",
        ]:
            model_name = node["inputs"].get("model_name")
            if model_name and model_name in MODEL_WEIGHTS:
                weights_to_download.append(MODEL_WEIGHTS[model_name])

                if "GroundingDINO" in model_name:
                    weights_to_download.append("bert-base-uncased")
