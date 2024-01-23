import subprocess
import time
import os
import json

from helpers.ComfyUI_Controlnet_Aux import ComfyUI_Controlnet_Aux
from helpers.ComfyUI_AnimateDiff_Evolved import ComfyUI_AnimateDiff_Evolved

WEIGHTS_MANIFEST_URL = (
    "https://weights.replicate.delivery/default/comfy-ui/weights.json"
)
WEIGHTS_MANIFEST_PATH = "weights.json"
BASE_URL = "https://weights.replicate.delivery/default/comfy-ui"
BASE_PATH = "ComfyUI/models"


class WeightsDownloader:
    def __init__(self):
        self.weights_map = self._initialize_weights_map()

    def _download_weights_manifest(self):
        manifest_path = os.path.join(WEIGHTS_MANIFEST_PATH)
        if not os.path.exists(manifest_path):
            print(f"Downloading weights manifest from {WEIGHTS_MANIFEST_URL}")
            start = time.time()
            subprocess.check_call(
                [
                    "pget",
                    "--log-level",
                    "warn",
                    "-f",
                    WEIGHTS_MANIFEST_URL,
                    manifest_path,
                ],
                close_fds=False,
            )
            print(
                f"downloading {WEIGHTS_MANIFEST_URL} took: {(time.time() - start):.2f}s"
            )
        else:
            print("Weights manifest file already exists")

    def _generate_weights_map(self, keys, dest):
        return {
            key: {
                "url": f"{BASE_URL}/{dest}/{key}.tar",
                "dest": f"{BASE_PATH}/{dest}",
            }
            for key in keys
        }

    def _initialize_weights_map(self):
        self._download_weights_manifest()

        if not os.path.exists(WEIGHTS_MANIFEST_PATH):
            raise FileNotFoundError("The weights manifest file does not exist.")
        with open(WEIGHTS_MANIFEST_PATH, "r") as f:
            self.weights_manifest = json.load(f)

        weights_map = {}
        for key in self.weights_manifest.keys():
            if key.isupper():
                weights_map.update(
                    self._generate_weights_map(self.weights_manifest[key], key.lower())
                )
        weights_map.update(ComfyUI_Controlnet_Aux.weights_map(BASE_URL))
        weights_map.update(ComfyUI_AnimateDiff_Evolved.weights_map(BASE_URL))
        print("Allowed weights:")
        for weight in weights_map.keys():
            print(weight)

        return weights_map

    def download_weights(self, weight_str):
        if weight_str in self.weights_map:
            self.download_if_not_exists(
                weight_str,
                self.weights_map[weight_str]["url"],
                self.weights_map[weight_str]["dest"],
            )
        else:
            raise ValueError(
                f"{weight_str} unavailable. View the list of available weights: https://github.com/fofr/cog-comfyui/blob/main/supported_weights.md"
            )

    def download_torch_checkpoints(self):
        self.download_if_not_exists(
            "mobilenet_v2-b0353104.pth",
            f"{BASE_URL}/custom_nodes/comfyui_controlnet_aux/mobilenet_v2-b0353104.pth.tar",
            "/root/.cache/torch/hub/checkpoints/",
        )

    def download_if_not_exists(self, weight_str, url, dest):
        if not os.path.exists(f"{dest}/{weight_str}"):
            self.download(weight_str, url, dest)

    def download(self, weight_str, url, dest):
        print(f"⏳ Downloading {weight_str}")
        start = time.time()
        subprocess.check_call(
            ["pget", "--log-level", "warn", "-xf", url, dest], close_fds=False
        )
        elapsed_time = time.time() - start
        file_size_bytes = os.path.getsize(f"{dest}/{weight_str}")
        file_size_megabytes = file_size_bytes / (1024 * 1024)
        print(f"⌛️ Download {weight_str} took: {elapsed_time:.2f}s, size: {file_size_megabytes:.2f}MB")

    def write_supported_weights(self):
        weight_lists = {
            "Checkpoints": self.weights_manifest.get("CHECKPOINTS", []),
            "Upscale models": self.weights_manifest.get("UPSCALE_MODELS", []),
            "CLIP Vision": self.weights_manifest.get("CLIP_VISION", []),
            "LORAs": self.weights_manifest.get("LORAS", []),
            "IPAdapter": self.weights_manifest.get("IPADAPTER", []),
            "ControlNet": self.weights_manifest.get("CONTROLNET", []),
            "VAE": self.weights_manifest.get("VAE", []),
            "PhotoMaker": self.weights_manifest.get("PHOTOMAKER", []),
            "AnimateDiff": ComfyUI_AnimateDiff_Evolved.models(),
            "AnimateDiff LORAs": ComfyUI_AnimateDiff_Evolved.loras(),
            "ControlNet Preprocessors": sorted(
                {
                    f"{repo}/{filename}"
                    for filename, repo in ComfyUI_Controlnet_Aux.models().items()
                }
            ),
        }
        with open("supported_weights.md", "w") as f:
            for weight_type, weights in weight_lists.items():
                f.write(f"## {weight_type}\n\n")
                for weight in weights:
                    f.write(f"- {weight}\n")
                f.write("\n")

    def print_weights_urls(self):
        weights_urls = [
            weight_info["url"] for weight_str, weight_info in self.weights_map.items()
        ]
        return weights_urls
