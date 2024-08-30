from custom_node_helper import CustomNodeHelper

RVM_MODELS = [
    "rvm_mobilenetv3_fp16.torchscript",
    "rvm_mobilenetv3_fp32.torchscript",
    "rvm_resnet50_fp16.torchscript",
    "rvm_resnet50_fp32.torchscript",
]

BRIAAI_MODELS = ["briaai_rmbg_v1.4.pth"]


class ComfyUI_Video_Matting(CustomNodeHelper):
    @staticmethod
    def models():
        return RVM_MODELS + BRIAAI_MODELS

    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type("BRIAAI Matting"):
            weights_to_download.extend(BRIAAI_MODELS)

        if node.is_type("Robust Video Matting"):
            weights_to_download.extend(RVM_MODELS)

    @staticmethod
    def weights_map(base_url):
        return {
            model: {
                "url": f"{base_url}/custom_nodes/ComfyUI-Video-Matting/ckpts/{model}.tar",
                "dest": "ComfyUI/custom_nodes/ComfyUI-Video-Matting/ckpts/",
            }
            for model in RVM_MODELS + BRIAAI_MODELS
        }
