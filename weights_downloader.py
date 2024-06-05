import subprocess
import time
import os
from weights_manifest import WeightsManifest


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

    def __init__(self):
        self.weights_manifest = WeightsManifest()
        self.weights_map = self.weights_manifest.weights_map

    def _run_pget(self, args, close_fds=False, timeout=None):
        try:
            output = subprocess.check_output(args, stderr=subprocess.STDOUT, close_fds=close_fds, universal_newlines=True, timeout=timeout)
        except subprocess.CalledProcessError as e:
            output = e.output
            if "permission denied" in output:
                pid_dir = os.getenv('XDG_RUNTIME_DIR', '/run/user/1000')
                if not os.access(pid_dir, os.W_OK):
                    pid_dir = os.path.expanduser("~")
                new_args = args[:1] + ["--pid-file", f"{pid_dir}/pget.pid"] + args[1:]
                try:
                    output = subprocess.check_output(new_args, stderr=subprocess.STDOUT, close_fds=close_fds, universal_newlines=True, timeout=timeout)
                except subprocess.CalledProcessError as e:
                    raise
            else:
                raise

    def get_weights_by_type(self, type):
        return self.weights_manifest.get_weights_by_type(type)

    def download_weights(self, weight_str):
        if weight_str in self.weights_map:
            if self.weights_manifest.is_non_commercial_only(weight_str):
                print(
                    f"⚠️  {weight_str} is for non-commercial use only. Unless you have obtained a commercial license.\nDetails: https://github.com/fofr/cog-comfyui/blob/main/weights_licenses.md"
                )

            if isinstance(self.weights_map[weight_str], list):
                for weight in self.weights_map[weight_str]:
                    self.download_if_not_exists(
                        weight_str, weight["url"], weight["dest"]
                    )
            else:
                self.download_if_not_exists(
                    weight_str,
                    self.weights_map[weight_str]["url"],
                    self.weights_map[weight_str]["dest"],
                )
        else:
            raise ValueError(
                f"{weight_str} unavailable. View the list of available weights: https://github.com/fofr/cog-comfyui/blob/main/supported_weights.md"
            )

    def download_if_not_exists(self, weight_str, url, dest):
        if dest.endswith(weight_str):
            path_string = dest
        else:
            path_string = os.path.join(dest, weight_str)

        if not os.path.exists(path_string):
            self.download(weight_str, url, dest)

    def download(self, weight_str, url, dest):
        if "/" in weight_str:
            subfolder = weight_str.rsplit("/", 1)[0]
            dest = os.path.join(dest, subfolder)
            os.makedirs(dest, exist_ok=True)

        print(f"⏳ Downloading {weight_str} to {dest}")
        start = time.time()
        self._run_pget(
            ["pget", "--log-level", "warn", "-xf", url, dest], close_fds=False
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
