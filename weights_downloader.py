import subprocess
import time
import os

from weights_manifest import WeightsManifest

BASE_URL = "https://weights.replicate.delivery/default/comfy-ui"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"


class WeightsDownloader:
    supported_filetypes = [
        ".ckpt",
        ".safetensors",
        ".pt",
        ".pth",
        ".bin",
        ".onnx",
        ".torchscript",
    ]

    valid_domains = [
        "https://huggingface.co/",
        "https://civitai.com/",
        "https://weights.replicate.delivery",
        "https://replicate.delivery",
    ]

    def __init__(self, bring_your_own_weights_manifest=None):
        self.weights_manifest = WeightsManifest(bring_your_own_weights_manifest)
        self.weights_map = self.weights_manifest.weights_map

    def get_weights_by_type(self, type):
        return self.weights_manifest.get_weights_by_type(type)

    def download_weights(self, weight_str):
        if weight_str in self.weights_map:
            if self.weights_manifest.is_non_commercial_only(weight_str):
                print(
                    f"⚠️  {weight_str} is for non-commercial use only. Unless you have obtained a commercial license.\nDetails: https://github.com/fofr/cog-comfyui/blob/main/weights_licenses.md"
                )
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
        if dest.endswith(weight_str):
            path_string = dest
        else:
            path_string = os.path.join(dest, weight_str)

        if not os.path.exists(path_string):
            self.download(weight_str, url, dest)

    def download(self, weight_str, url, dest):
        is_archive = weight_str.endswith(".tar")

        if not any(url.startswith(domain) for domain in self.valid_domains):
            raise ValueError(
                f"URL must be on one of the valid domains: {self.valid_domains}"
            )

        if "/" in weight_str:
            subfolder = weight_str.rsplit("/", 1)[0]
            dest = os.path.join(dest, subfolder)
            os.makedirs(dest, exist_ok=True)

        print(f"⏳ Downloading {weight_str} to {dest}")
        start = time.time()
        subprocess.check_call(
            ["pget", "--log-level", "warn", "-xf" if is_archive else "-f", url, dest],
            close_fds=False,
        )
        elapsed_time = time.time() - start
        try:
            file_size_bytes = os.path.getsize(
                os.path.join(dest, os.path.basename(weight_str))
            )
            file_size_megabytes = file_size_bytes / (1024 * 1024)
            print(
                f"⌛️ Downloaded {weight_str} in {elapsed_time:.2f}s, size: {file_size_megabytes:.2f}MB"
            )
        except FileNotFoundError:
            print(f"⌛️ Downloaded {weight_str} in {elapsed_time:.2f}s")
