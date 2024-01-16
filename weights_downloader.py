import subprocess
import time
import os

BASE_URL = "https://weights.replicate.delivery/default/comfy-ui"
BASE_PATH = "ComfyUI/models"

CHECKPOINTS = [
    "sd_xl_base_1.0.safetensors",
    "sd_xl_refiner_1.0.safetensors",
    "sd_xl_turbo_1.0_fp16.safetensors",
    "v2-1_768-ema-pruned.ckpt",
    "v1-5-pruned-emaonly.ckpt",
    "512-inpainting-ema.safetensors",
    "svd.safetensors",
    "svd_xt.safetensors",
    # civit ai
    "turbovisionxlSuperFastXLBasedOnNew_tvxlV32Bakedvae.safetensors",
]
UPSCALE_MODELS = [
    "RealESRGAN_x2.pth",
    "RealESRGAN_x4.pth",
    "RealESRGAN_x8.pth",
    "RealESRGAN_x4plus.pth",
]
CLIP_VISION = [
    "clip_vision_g.safetensors",
    # https://huggingface.co/h94/IP-Adapter/blob/main/models/image_encoder/model.safetensors
    "model.15.safetensors",
    # https://huggingface.co/h94/IP-Adapter/blob/main/sdxl_models/image_encoder/model.safetensors
    "model.sdxl.safetensors",
]
LORAS = [
    "lcm_lora_sdxl.safetensors",
    "lcm-lora-sdv1-5.safetensors",
    "lcm-lora-ssd-1b.safetensors",
]
CONTROLNET = [
    "controlnet-canny-sdxl-1.0.fp16.safetensors",
    "controlnet-depth-sdxl-1.0.fp16.safetensors",
    "thibaud_xl_openpose.safetensors",
]
IPADAPTER = [
    "ip-adapter-plus-face_sdxl_vit-h.bin",
    "ip-adapter-plus-face_sdxl_vit-h.safetensors",
    "ip-adapter-plus_sdxl_vit-h.bin",
    "ip-adapter-plus_sdxl_vit-h.safetensors",
]

CONTROLNET_AUX_MODELS = {
    "dw-ll_ucoco_384.onnx": "yzd-v/DWPose",
    "yolox_l.onnx": "yzd-v/DWPose",
    "ZoeD_M12_N.pt": "lllyasviel/Annotators",
}


def generate_weights_map(keys, dest):
    return {
        key: {
            "url": f"{BASE_URL}/{dest}/{key}.tar",
            "dest": f"{BASE_PATH}/{dest}",
        }
        for key in keys
    }


def generate_controlnet_aux_weights_map(keys):
    return {
        key: {
            "url": f"{BASE_URL}/comfyui_controlnet_aux/{key}.tar",
            "dest": f"ComfyUI/custom_nodes/comfyui_controlnet_aux/ckpts/{keys[key]}",
        }
        for key in keys
    }


WEIGHTS_MAP = {
    **generate_weights_map(CHECKPOINTS, "checkpoints"),
    **generate_weights_map(UPSCALE_MODELS, "upscale_models"),
    **generate_weights_map(CLIP_VISION, "clip_vision"),
    **generate_weights_map(LORAS, "loras"),
    **generate_weights_map(IPADAPTER, "ipadapter"),
    **generate_weights_map(CONTROLNET, "controlnet"),
    **generate_controlnet_aux_weights_map(CONTROLNET_AUX_MODELS),
}


class WeightsDownloader:
    @staticmethod
    def download_weights(weight_str):
        if weight_str in WEIGHTS_MAP:
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
    def download_torch_checkpoints():
        WeightsDownloader.download_if_not_exists(
            "mobilenet_v2-b0353104.pth",
            f"{BASE_URL}/comfyui_controlnet_aux/mobilenet_v2-b0353104.pth.tar",
            "/root/.cache/torch/hub/checkpoints/"
        )

    @staticmethod
    def download_if_not_exists(weight_str, url, dest):
        if not os.path.exists(f"{dest}/{weight_str}"):
            WeightsDownloader.download(weight_str, url, dest)

    @staticmethod
    def download(weight_str, url, dest):
        start = time.time()
        subprocess.check_call(["pget", "--log-level", "warn", "-xf", url, dest], close_fds=False)
        print(f"downloading {weight_str} took: {(time.time() - start):.2f}s")
