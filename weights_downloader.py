import subprocess
import time
import os

BASE_URL = "https://weights.replicate.delivery/default/comfy-ui"
BASE_PATH = "ComfyUI/models"

CHECKPOINTS = [
    "sd_xl_base_1.0.safetensors",
    "sd_xl_refiner_1.0.safetensors",
    "v1-5-pruned-emaonly.ckpt",
    "512-inpainting-ema.safetensors",
]
UPSCALE_MODELS = ["RealESRGAN_x2.pth", "RealESRGAN_x4.pth", "RealESRGAN_x8.pth"]
CLIP_VISION = ["clip_vision_g.safetensors"]
LORAS = ["lcm_lora_sdxl.safetensors"]


def generate_weights_map(keys, dest):
    return {
        key: {
            "url": f"{BASE_URL}/{os.path.splitext(key)[0]}.tar",
            "dest": f"{BASE_PATH}/{dest}",
        }
        for key in keys
    }


WEIGHTS_MAP = {
    **generate_weights_map(CHECKPOINTS, "checkpoints"),
    **generate_weights_map(UPSCALE_MODELS, "upscale_models"),
    **generate_weights_map(CLIP_VISION, "clip_vision"),
    **generate_weights_map(LORAS, "loras"),
}


class WeightsDownloader:
    @staticmethod
    def download_weights(weight_str):
        if weight_str in WEIGHTS_MAP:
            print(f"Weights {weight_str} are available")
            WeightsDownloader.download_if_not_exists(
                weight_str,
                WEIGHTS_MAP[weight_str]["url"],
                WEIGHTS_MAP[weight_str]["dest"],
            )
        else:
            raise ValueError(
                f"{weight_str} not available. Available weights are: {', '.join(WEIGHTS_MAP.keys())}"
            )

    @staticmethod
    def download_if_not_exists(weight_str, url, dest):
        if not os.path.exists(f"{dest}/{weight_str}"):
            WeightsDownloader.download(url, dest)

    @staticmethod
    def download(url, dest):
        start = time.time()
        print("downloading url: ", url)
        print("downloading to: ", dest)
        subprocess.check_call(["pget", "-xf", url, dest], close_fds=False)
        print("downloading took: ", time.time() - start)
