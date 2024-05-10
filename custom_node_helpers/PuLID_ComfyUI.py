import site
from custom_node_helper import CustomNodeHelper

HUGGINGFACE_CACHE_PATH = "/root/.cache/huggingface/hub"
PACKAGE_ROOT_PATH = site.getsitepackages()[0]
FACEXLIB_PATH = f"{PACKAGE_ROOT_PATH}/facexlib/weights"
BASE_FILE_PATH = "https://weights.replicate.delivery/default/comfy-ui"

facexlib_models = [
    "detection_Resnet50_Final.pth",
    "parsing_bisenet.pth",
    "parsing_parsenet.pth",
]

eva_clip_model = "models--QuanSun--EVA-CLIP"


class PuLID_ComfyUI(CustomNodeHelper):
    @staticmethod
    def add_weights(weights_to_download, node):
        if node.is_type_in(["PulidEvaClipLoader", "ApplyPulid"]):
            from weights_downloader import WeightsDownloader

            weights_downloader = WeightsDownloader()

            if node.is_type("PulidEvaClipLoader"):
                weights_downloader.download_if_not_exists(
                    eva_clip_model,
                    f"{BASE_FILE_PATH}/clip/{eva_clip_model}.tar",
                    f"{HUGGINGFACE_CACHE_PATH}/{eva_clip_model}",
                )

            if node.is_type("ApplyPulid"):
                for file in facexlib_models:
                    weights_downloader.download_if_not_exists(
                        file,
                        f"{BASE_FILE_PATH}/facedetection/{file}.tar",
                        FACEXLIB_PATH,
                    )
        elif node.is_type("PulidInsightFaceLoader"):
            weights_to_download.append("models/antelopev2")
