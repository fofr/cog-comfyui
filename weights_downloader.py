import subprocess
import time
import os
import shutil

BASE_URL = "https://weights.replicate.delivery/default/comfy-ui"
BASE_PATH = "ComfyUI/models"

WEIGHTS_MAP = {
    "v1-5-pruned-emaonly.ckpt": {
        "url": f"{BASE_URL}/v1-5-pruned-emaonly.tar",
        "dest": f"{BASE_PATH}/checkpoints",
    }
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
