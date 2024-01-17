import subprocess
import time
import os

from helpers.ComfyUI_Controlnet_Aux import ComfyUI_Controlnet_Aux
from helpers.ComfyUI_AnimateDiff_Evolved import ComfyUI_AnimateDiff_Evolved

BASE_URL = "https://weights.replicate.delivery/default/comfy-ui"
BASE_PATH = "ComfyUI/models"

CHECKPOINTS = [
    "512-inpainting-ema.safetensors",
    "Deliberate_v2.safetensors",
    "DreamShaper_6.2_BakedVae_pruned.safetensors",
    "DreamShaper_6.31_BakedVae.safetensors",
    "DreamShaper_6.31_BakedVae_pruned.safetensors",
    "DreamShaper_6.31_INPAINTING.inpainting.safetensors",
    "DreamShaper_6_BakedVae.safetensors",
    "LCM_Dreamshaper_v7_4k.safetensors",
    "RealVisXL_V2.0.safetensors",
    "RealVisXL_V3.0.safetensors",
    "RealVisXL_V3.0_Turbo.safetensors",
    "Realistic_Vision_V5.1-inpainting.ckpt",
    "Realistic_Vision_V5.1-inpainting.safetensors",
    "Realistic_Vision_V5.1.ckpt",
    "Realistic_Vision_V5.1.safetensors",
    "Realistic_Vision_V5.1_fp16-no-ema-inpainting.ckpt",
    "Realistic_Vision_V5.1_fp16-no-ema-inpainting.safetensors",
    "Realistic_Vision_V5.1_fp16-no-ema.ckpt",
    "Realistic_Vision_V5.1_fp16-no-ema.safetensors",
    "Realistic_Vision_V6.0_NV_B1.safetensors",
    "Realistic_Vision_V6.0_NV_B1_fp16.safetensors",
    "Realistic_Vision_V6.0_NV_B1_inpainting.safetensors",
    "Realistic_Vision_V6.0_NV_B1_inpainting_fp16.safetensors",
    "SSD-1B.safetensors",
    "sd_xl_base_1.0.safetensors",
    "sd_xl_refiner_1.0.safetensors",
    "sd_xl_turbo_1.0_fp16.safetensors",
    "svd.safetensors",
    "svd_xt.safetensors",
    "turbovisionxlSuperFastXLBasedOnNew_tvxlV32Bakedvae.safetensors",
    "v1-5-pruned-emaonly.ckpt",
    "v2-1_768-ema-pruned.ckpt",
    "v2-1_768-ema-pruned.safetensors",
    "v2-1_768-nonema-pruned.ckpt",
    "v2-1_768-nonema-pruned.safetensors",
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

# https://huggingface.co/lllyasviel/sd_control_collection/tree/main
# https://huggingface.co/lllyasviel/ControlNet-v1-1/tree/main
# https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors
CONTROLNET = [
    "control_lora_rank128_v11e_sd15_ip2p_fp16.safetensors",
    "control_lora_rank128_v11e_sd15_shuffle_fp16.safetensors",
    "control_lora_rank128_v11f1e_sd15_tile_fp16.safetensors",
    "control_lora_rank128_v11f1p_sd15_depth_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_canny_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_inpaint_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_lineart_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_mlsd_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_normalbae_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_openpose_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_scribble_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_seg_fp16.safetensors",
    "control_lora_rank128_v11p_sd15_softedge_fp16.safetensors",
    "control_lora_rank128_v11p_sd15s2_lineart_anime_fp16.safetensors",
    "control_v11e_sd15_ip2p.pth",
    "control_v11e_sd15_ip2p_fp16.safetensors",
    "control_v11e_sd15_shuffle.pth",
    "control_v11e_sd15_shuffle_fp16.safetensors",
    "control_v11f1e_sd15_tile.pth",
    "control_v11f1e_sd15_tile_fp16.safetensors",
    "control_v11f1p_sd15_depth.pth",
    "control_v11f1p_sd15_depth_fp16.safetensors",
    "control_v11p_sd15_canny.pth",
    "control_v11p_sd15_canny_fp16.safetensors",
    "control_v11p_sd15_inpaint.pth",
    "control_v11p_sd15_inpaint_fp16.safetensors",
    "control_v11p_sd15_lineart.pth",
    "control_v11p_sd15_lineart_fp16.safetensors",
    "control_v11p_sd15_mlsd.pth",
    "control_v11p_sd15_mlsd_fp16.safetensors",
    "control_v11p_sd15_normalbae.pth",
    "control_v11p_sd15_normalbae_fp16.safetensors",
    "control_v11p_sd15_openpose.pth",
    "control_v11p_sd15_openpose_fp16.safetensors",
    "control_v11p_sd15_scribble.pth",
    "control_v11p_sd15_scribble_fp16.safetensors",
    "control_v11p_sd15_seg.pth",
    "control_v11p_sd15_seg_fp16.safetensors",
    "control_v11p_sd15_softedge.pth",
    "control_v11p_sd15_softedge_fp16.safetensors",
    "control_v11p_sd15s2_lineart_anime.pth",
    "control_v11p_sd15s2_lineart_anime_fp16.safetensors",
    "control_v11u_sd15_tile_fp16.safetensors",
    "controlnet-canny-sdxl-1.0.fp16.safetensors",
    "controlnet-depth-sdxl-1.0.fp16.safetensors",
    "diffusers_xl_canny_full.safetensors",
    "diffusers_xl_canny_mid.safetensors",
    "diffusers_xl_canny_small.safetensors",
    "diffusers_xl_depth_full.safetensors",
    "diffusers_xl_depth_mid.safetensors",
    "diffusers_xl_depth_small.safetensors",
    "ioclab_sd15_recolor.safetensors",
    "ip-adapter_sd15.pth",
    "ip-adapter_sd15_plus.pth",
    "ip-adapter_xl.pth",
    "kohya_controllllite_xl_blur.safetensors",
    "kohya_controllllite_xl_blur_anime.safetensors",
    "kohya_controllllite_xl_blur_anime_beta.safetensors",
    "kohya_controllllite_xl_canny.safetensors",
    "kohya_controllllite_xl_canny_anime.safetensors",
    "kohya_controllllite_xl_depth.safetensors",
    "kohya_controllllite_xl_depth_anime.safetensors",
    "kohya_controllllite_xl_openpose_anime.safetensors",
    "kohya_controllllite_xl_openpose_anime_v2.safetensors",
    "kohya_controllllite_xl_scribble_anime.safetensors",
    "sai_xl_canny_128lora.safetensors",
    "sai_xl_canny_256lora.safetensors",
    "sai_xl_depth_128lora.safetensors",
    "sai_xl_depth_256lora.safetensors",
    "sai_xl_recolor_128lora.safetensors",
    "sai_xl_recolor_256lora.safetensors",
    "sai_xl_sketch_128lora.safetensors",
    "sai_xl_sketch_256lora.safetensors",
    "sargezt_xl_depth.safetensors",
    "sargezt_xl_depth_faid_vidit.safetensors",
    "sargezt_xl_depth_zeed.safetensors",
    "sargezt_xl_softedge.safetensors",
    "t2i-adapter_diffusers_xl_canny.safetensors",
    "t2i-adapter_diffusers_xl_depth_midas.safetensors",
    "t2i-adapter_diffusers_xl_depth_zoe.safetensors",
    "t2i-adapter_diffusers_xl_lineart.safetensors",
    "t2i-adapter_diffusers_xl_openpose.safetensors",
    "t2i-adapter_diffusers_xl_sketch.safetensors",
    "t2i-adapter_xl_canny.safetensors",
    "t2i-adapter_xl_openpose.safetensors",
    "t2i-adapter_xl_sketch.safetensors",
    "thibaud_xl_openpose.safetensors",
    "thibaud_xl_openpose_256lora.safetensors",
]
IPADAPTER = [
    "ip-adapter-faceid-plus_sd15.bin",
    "ip-adapter-faceid-plus_sd15_lora.safetensors",
    "ip-adapter-faceid-plusv2_sd15.bin",
    "ip-adapter-faceid-plusv2_sd15_lora.safetensors",
    "ip-adapter-faceid-plusv2_sdxl.bin",
    "ip-adapter-faceid-plusv2_sdxl_lora.safetensors",
    "ip-adapter-faceid_sd15.bin",
    "ip-adapter-faceid_sd15_lora.safetensors",
    "ip-adapter-faceid_sdxl.bin",
    "ip-adapter-faceid_sdxl_lora.safetensors",
    "ip-adapter-full-face_sd15.bin",
    "ip-adapter-full-face_sd15.safetensors",
    "ip-adapter-plus-face_sd15.bin",
    "ip-adapter-plus-face_sd15.safetensors",
    "ip-adapter-plus-face_sdxl_vit-h.bin",
    "ip-adapter-plus-face_sdxl_vit-h.safetensors",
    "ip-adapter-plus_sd15.bin",
    "ip-adapter-plus_sd15.safetensors",
    "ip-adapter-plus_sdxl_vit-h.bin",
    "ip-adapter-plus_sdxl_vit-h.safetensors",
    "ip-adapter_sd15.bin",
    "ip-adapter_sd15.safetensors",
    "ip-adapter_sd15_light.bin",
    "ip-adapter_sd15_light.safetensors",
    "ip-adapter_sd15_vit-G.bin",
    "ip-adapter_sd15_vit-G.safetensors",
]

VAE = [
    "vae-ft-mse-840000-ema-pruned.safetensors",
]


def generate_weights_map(keys, dest):
    return {
        key: {
            "url": f"{BASE_URL}/{dest}/{key}.tar",
            "dest": f"{BASE_PATH}/{dest}",
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
    **generate_weights_map(VAE, "vae"),
    **ComfyUI_Controlnet_Aux.weights_map(BASE_URL),
    **ComfyUI_AnimateDiff_Evolved.weights_map(BASE_URL),
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
            f"{BASE_URL}/custom_nodes/comfyui_controlnet_aux/mobilenet_v2-b0353104.pth.tar",
            "/root/.cache/torch/hub/checkpoints/",
        )

    @staticmethod
    def download_if_not_exists(weight_str, url, dest):
        if not os.path.exists(f"{dest}/{weight_str}"):
            WeightsDownloader.download(weight_str, url, dest)

    @staticmethod
    def download(weight_str, url, dest):
        start = time.time()
        subprocess.check_call(
            ["pget", "--log-level", "warn", "-xf", url, dest], close_fds=False
        )
        print(f"downloading {weight_str} took: {(time.time() - start):.2f}s")

    @staticmethod
    def write_supported_weights():
        weight_lists = {
            "Checkpoints": CHECKPOINTS,
            "Upscale models": UPSCALE_MODELS,
            "CLIP Vision": CLIP_VISION,
            "LORAs": LORAS,
            "IPAdapter": IPADAPTER,
            "ControlNet": CONTROLNET,
            "VAE": VAE,
            "AnimateDiff": ComfyUI_AnimateDiff_Evolved.models(),
            "AnimateDiff LORAs": ComfyUI_AnimateDiff_Evolved.loras(),
        }
        with open("supported_weights.md", "w") as f:
            for weight_type, weights in weight_lists.items():
                f.write(f"## {weight_type}\n\n")
                for weight in weights:
                    f.write(f"- {weight}\n")
                f.write("\n")

    @staticmethod
    def print_weights_urls():
        weights_urls = [
            weight_info["url"] for weight_str, weight_info in WEIGHTS_MAP.items()
        ]
        return weights_urls
