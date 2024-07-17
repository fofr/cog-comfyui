import subprocess
import time
import os
import json
import custom_node_helpers as helpers
from config import config

USER_WEIGHTS_MANIFEST_PATH = config["USER_WEIGHTS_MANIFEST_PATH"]
REMOTE_WEIGHTS_MANIFEST_URL = config["REMOTE_WEIGHTS_MANIFEST_URL"]
REMOTE_WEIGHTS_MANIFEST_PATH = "updated_weights.json"
WEIGHTS_MANIFEST_PATH = "weights.json"
BASE_URL = config["WEIGHTS_BASE_URL"]
MODELS_PATH = config["MODELS_PATH"]


class WeightsManifest:
    @staticmethod
    def base_url():
        return BASE_URL

    def __init__(self):
        self.download_latest_weights_manifest = (
            os.getenv("DOWNLOAD_LATEST_WEIGHTS_MANIFEST", "false").lower() == "true"
        )
        self.weights_manifest = self._load_weights_manifest()
        self.weights_map = self._initialize_weights_map()

    def _load_weights_manifest(self):
        if self.download_latest_weights_manifest:
            self._download_updated_weights_manifest()
        return self._merge_manifests()

    def _download_updated_weights_manifest(self):
        if not os.path.exists(REMOTE_WEIGHTS_MANIFEST_PATH):
            print(
                f"Downloading updated weights manifest from {REMOTE_WEIGHTS_MANIFEST_URL}"
            )
            start = time.time()
            try:
                subprocess.check_call(
                    [
                        "pget",
                        "--log-level",
                        "warn",
                        "-f",
                        REMOTE_WEIGHTS_MANIFEST_URL,
                        REMOTE_WEIGHTS_MANIFEST_PATH,
                    ],
                    close_fds=False,
                    timeout=5,
                )
                print(
                    f"Downloading {REMOTE_WEIGHTS_MANIFEST_URL} took: {(time.time() - start):.2f}s"
                )
            except subprocess.CalledProcessError:
                print(f"Failed to download {REMOTE_WEIGHTS_MANIFEST_URL}")
                pass
            except subprocess.TimeoutExpired:
                print(f"Download from {REMOTE_WEIGHTS_MANIFEST_URL} timed out")
                pass

    def _merge_manifests(self):
        if os.path.exists(WEIGHTS_MANIFEST_PATH):
            with open(WEIGHTS_MANIFEST_PATH, "r") as f:
                original_manifest = json.load(f)
        else:
            original_manifest = {}

        manifests_to_merge = [
            REMOTE_WEIGHTS_MANIFEST_PATH,
            USER_WEIGHTS_MANIFEST_PATH,
        ]

        for manifest_path in manifests_to_merge:
            if os.path.exists(manifest_path):
                with open(manifest_path, "r") as f:
                    manifest_to_merge = json.load(f)
                    for key in manifest_to_merge:
                        if key in original_manifest:
                            for item in manifest_to_merge[key]:
                                if item not in original_manifest[key]:
                                    print(f"Adding {item} to {key}")
                                    original_manifest[key].append(item)
                        else:
                            original_manifest[key] = manifest_to_merge[key]

        return original_manifest

    def _initialize_weights_map(self):
        weights_map = {}

        def generate_weights_map(keys, dest):
            return {
                key: {
                    "url": f"{BASE_URL}/{dest}/{key}.tar",
                    "dest": f"{MODELS_PATH}/{dest}",
                }
                for key in keys
            }

        def update_weights_map(source_map):
            for k, v in source_map.items():
                if k in weights_map:
                    if isinstance(weights_map[k], list):
                        weights_map[k].append(v)
                    else:
                        weights_map[k] = [weights_map[k], v]
                else:
                    weights_map[k] = v

        for key in self.weights_manifest.keys():
            directory_name = "LLM" if key == "LLM" else key.lower()
            map = generate_weights_map(self.weights_manifest[key], directory_name)
            update_weights_map(map)

        for module_name in dir(helpers):
            module = getattr(helpers, module_name)
            if hasattr(module, "weights_map"):
                map = module.weights_map(BASE_URL)
                update_weights_map(map)

        return weights_map

    def non_commercial_weights(self):
        return [
            "inswapper_128.onnx",
            "inswapper_128_fp16.onnx",
            "proteus_v02.safetensors",
            "RealVisXL_V3.0_Turbo.safetensors",
            "sd_xl_turbo_1.0.safetensors",
            "sd_xl_turbo_1.0_fp16.safetensors",
            "svd.safetensors",
            "svd_xt.safetensors",
            "turbovisionxlSuperFastXLBasedOnNew_tvxlV32Bakedvae",
            "copaxTimelessxlSDXL1_v8.safetensors",
            "MODILL_XL_0.27_RC.safetensors",
            "epicrealismXL_v10.safetensors",
            "RMBG-1.4/model.pth",
            "GPEN-BFR-1024.onnx",
            "GPEN-BFR-2048.onnx",
            "GPEN-BFR-512.onnx",
            "stable_cascade_stage_b.safetensors",
            "stable_cascade_stage_c.safetensors",
            "stable-cascade/stage_b.safetensors",
            "stable-cascade/stage_b_bf16.safetensors",
            "stable-cascade/stage_b_lite.safetensors",
            "stable-cascade/stage_b_lite_bf16.safetensors",
            "stable-cascade/stage_c.safetensors",
            "stable-cascade/stage_c_bf16.safetensors",
            "stable-cascade/stage_c_lite.safetensors",
            "stable-cascade/stage_c_lite_bf16.safetensors",
            "stable-cascade/effnet_encoder.safetensors",
            "stable-cascade/stage_a.safetensors",
        ]

    def is_non_commercial_only(self, weight_str):
        return weight_str in self.non_commercial_weights()

    def get_weights_by_type(self, weight_type):
        return self.weights_manifest.get(weight_type, [])
