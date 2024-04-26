#!/usr/bin/env python
import argparse
import subprocess
import os
import sys
import json


def download_file(url, filename=None):
    if not filename and "huggingface.co" in url:
        filename = url.split("/")[-1]
        filename = filename.rstrip("?download=true")
    if filename:
        print(f"Downloading {url} to {filename}")
        subprocess.run(["wget", url, "-O", filename])
    else:
        print(f"Downloading {url} (no filename)")
        subprocess.run(["wget", url])
        exit(1)
    print(f"Successfully downloaded {filename}")
    return filename


def tar_file(filename):
    tar_filename = filename + ".tar"
    subprocess.run(["tar", "-cvf", tar_filename, filename])
    print(f"Tarred {filename} to {tar_filename}")
    return tar_filename


def upload_to_gcloud(local_file, destination_blob_name, subfolder):
    destination_path = (
        f"{destination_blob_name}/{subfolder}/{local_file}"
        if subfolder
        else f"{destination_blob_name}/{local_file}"
    )
    print(f"Uploading {local_file} to {destination_path}")
    subprocess.run(["gcloud", "storage", "cp", local_file, destination_path])
    print(f"Successfully uploaded to {destination_path}")


def remove_files(*filenames):
    print(f"About to remove the following files: {', '.join(filenames)}")
    for filename in filenames:
        os.remove(filename)
        print(f"Successfully removed {filename}")


def get_subfolder():
    subfolders = [
        "checkpoints",
        "upscale_models",
        "clip_vision",
        "loras",
        "embeddings",
        "controlnet",
        "ipadapter",
        "vae",
        "unet",
        "photomaker",
        "instantid",
        "insightface",
        "facedetection",
        "facerestore_models",
        "mmdets",
        "sams",
        "grounding-dino",
        "ultralytics",
        "custom_nodes/ComfyUI-AnimateDiff-Evolved",
        "custom_nodes/comfyui_controlnet_aux",
        "Other",
    ]
    for i, subfolder in enumerate(subfolders, start=1):
        print(f"{i}. {subfolder}")
    choice = int(
        input("Choose the type of file by selecting the corresponding number: ")
    )
    if choice == len(subfolders):
        return input("Enter the subfolder name: ")
    else:
        return subfolders[choice - 1]


def update_weights_json(subfolder, filename):
    subfolder = subfolder.upper()
    with open("weights.json", "r+") as f:
        weights_data = json.load(f)
        if subfolder in weights_data:
            if filename not in weights_data[subfolder]:
                weights_data[subfolder].append(filename)
                f.seek(0)
                json.dump(weights_data, f, indent=4)
                f.truncate()
                print(f"Added {filename} to {subfolder} in weights.json")
            else:
                print(f"{filename} already exists in {subfolder} in weights.json")
        else:
            print(f"{subfolder} not found in weights.json")


def process_file(url=None, filename=None, subfolder=None):
    if url:
        print(f"Processing {url}")
        local_file = download_file(url, filename)
    else:
        print(f"Processing {filename}")
        local_file = filename
    tarred_file = tar_file(local_file)
    upload_to_gcloud(tarred_file, "gs://replicate-weights/comfy-ui", subfolder)
    update_weights_json(subfolder, local_file)
    remove_files(local_file, tarred_file)
    subprocess.run(["python", "scripts/sort_weights.py"])


def process_weights_file(weights_file, subfolder=None):
    with open(weights_file, "r") as f:
        for line in f:
            url, filename = line.strip().split()
            process_file(url, filename, subfolder)


def main():
    parser = argparse.ArgumentParser(
        description="Download a file, tar it, and upload to Google Cloud Storage"
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="The URL of the file to download or the local file to process",
    )
    parser.add_argument(
        "filename",
        nargs="?",
        help="The local filename to save the file as. Defaults to the filename in the URL",
    )
    parser.add_argument(
        "--weights_list",
        help="The weights list file with URLs to download",
    )
    args = parser.parse_args()

    subfolder = get_subfolder()

    if args.weights_list:
        process_weights_file(args.weights_list, subfolder)
    elif args.file:
        filename = args.filename if args.filename else args.file
        if args.file.startswith(("http://", "https://")):
            process_file(url=args.file, filename=filename, subfolder=subfolder)
        elif os.path.isfile(args.file):
            process_file(filename=filename, subfolder=subfolder)
        else:
            print(f"Error: The file or URL {args.file} is not valid.")
            sys.exit(1)


if __name__ == "__main__":
    main()
