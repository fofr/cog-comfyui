import os
import argparse
import shutil

# Define the file types to be removed
file_types = [
    ".bin",
    ".safetensors",
    ".ckpt",
    ".pt",
    ".pth",
    ".onnx",
    ".torchscript",
]

# Define the whitelist of files to be preserved
whitelist = [
    "./ComfyUI/custom_nodes/efficiency-nodes-comfyui/py/sd15_resizer.pt",
    "./ComfyUI/custom_nodes/efficiency-nodes-comfyui/py/sdxl_resizer.pt",
    "./ComfyUI/custom_nodes/comfyui_controlnet_aux/src/custom_mesh_graphormer/modeling/data/mano_195_adjmat_indices.pt",
    "./ComfyUI/custom_nodes/comfyui_controlnet_aux/src/custom_mesh_graphormer/modeling/data/smpl_431_adjmat_values.pt",
    "./ComfyUI/custom_nodes/comfyui_controlnet_aux/src/custom_mesh_graphormer/modeling/data/mano_195_adjmat_size.pt",
    "./ComfyUI/custom_nodes/comfyui_controlnet_aux/src/custom_mesh_graphormer/modeling/data/smpl_431_adjmat_size.pt",
    "./ComfyUI/custom_nodes/comfyui_controlnet_aux/src/custom_mesh_graphormer/modeling/data/mano_195_adjmat_values.pt",
    "./ComfyUI/custom_nodes/comfyui_controlnet_aux/src/custom_mesh_graphormer/modeling/data/smpl_431_adjmat_indices.pt",
]

def remove_model_files(directory, dry_run=False):
    # Remove specified file types and preserve whitelist
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file.endswith(file_type) for file_type in file_types) and file_path not in whitelist:
                if dry_run:
                    print(f"Will remove file: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")

    # Remove contents of ComfyUI/output and ComfyUI/input
    comfyui_dirs = ['./ComfyUI/output', './ComfyUI/input']
    for comfyui_dir in comfyui_dirs:
        if os.path.exists(comfyui_dir):
            if dry_run:
                print(f"Will remove contents of directory: {comfyui_dir}")
            else:
                shutil.rmtree(comfyui_dir)
                os.makedirs(comfyui_dir)
                print(f"Removed contents of directory: {comfyui_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove model files from a directory and clear ComfyUI directories.")
    parser.add_argument("directory", nargs='?', default='.', type=str, help="Directory to remove files from. Defaults to the current directory.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Perform a dry run without deleting files.",
    )
    args = parser.parse_args()

    remove_model_files(args.directory, dry_run=args.dry_run)
