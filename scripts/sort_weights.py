#!/usr/bin/env python3

import json
import os
import sys

# Ensure the script can import WeightsManifest from the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from weights_manifest import WeightsManifest
import custom_node_helpers as helpers


def write_supported_weights():
    weights_manifest = WeightsManifest()
    weight_lists = {
        "Checkpoints": weights_manifest.get_weights_by_type("CHECKPOINTS"),
        "Upscale models": weights_manifest.get_weights_by_type("UPSCALE_MODELS"),
        "CLIP": weights_manifest.get_weights_by_type("CLIP"),
        "CLIP Vision": weights_manifest.get_weights_by_type("CLIP_VISION"),
        "LORAs": weights_manifest.get_weights_by_type("LORAS"),
        "Embeddings": weights_manifest.get_weights_by_type("EMBEDDINGS"),
        "IPAdapter": weights_manifest.get_weights_by_type("IPADAPTER"),
        "ControlNet": weights_manifest.get_weights_by_type("CONTROLNET"),
        "VAE": weights_manifest.get_weights_by_type("VAE"),
        "UNets": weights_manifest.get_weights_by_type("UNET"),
        "PhotoMaker": weights_manifest.get_weights_by_type("PHOTOMAKER"),
        "InstantID": weights_manifest.get_weights_by_type("INSTANTID"),
        "InsightFace": weights_manifest.get_weights_by_type("INSIGHTFACE"),
        "Ultralytics": weights_manifest.get_weights_by_type("ULTRALYTICS"),
        "Segment anything models (SAM)": weights_manifest.get_weights_by_type("SAMS"),
        "GroundingDino": weights_manifest.get_weights_by_type("GROUNDING-DINO"),
        "MMDets": weights_manifest.get_weights_by_type("MMDETS"),
        "Face restoration models": weights_manifest.get_weights_by_type(
            "FACERESTORE_MODELS"
        ),
        "Face detection models": weights_manifest.get_weights_by_type("FACEDETECTION"),
        "LayerDiffusion": weights_manifest.get_weights_by_type("LAYER_MODEL"),
        "CLIP Segmentation": weights_manifest.get_weights_by_type("CLIPSEG"),
        "REMBG (Remove background)": weights_manifest.get_weights_by_type("REMBG"),
        "PuLID": weights_manifest.get_weights_by_type("PULID"),
        "GLIGEN": weights_manifest.get_weights_by_type("GLIGEN"),
        "Anyline": helpers.ComfyUI_Anyline.models(),
        "AnimateDiff": weights_manifest.get_weights_by_type("ANIMATEDIFF_MODELS"),
        "AnimateDiff LORAs": weights_manifest.get_weights_by_type(
            "ANIMATEDIFF_MOTION_LORA"
        ),
        "Frame Interpolation": helpers.ComfyUI_Frame_Interpolation.models(),
        "ControlNet Preprocessors": sorted(
            {
                f"{repo}/{filename}"
                for filename, repo in helpers.ComfyUI_Controlnet_Aux.models().items()
            }
        ),
    }
    with open("supported_weights.md", "w") as f:
        for weight_type, weights in weight_lists.items():
            f.write(f"## {weight_type}\n\n")
            for weight in weights:
                f.write(f"- {weight}\n")
            f.write("\n")


def main():
    # Load the JSON data from a file
    with open("weights.json", "r") as file:
        data = json.load(file)

    # Sort each array in the JSON data
    for key in data:
        if isinstance(data[key], list):
            data[key].sort(key=str.casefold)

    # Write the sorted JSON data back to the file
    with open("weights.json", "w") as file:
        json.dump(data, file, indent=2)

    # Write the supported weights to a markdown file
    write_supported_weights()


if __name__ == "__main__":
    main()
