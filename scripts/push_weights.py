#!/usr/bin/env python
import argparse
import subprocess
import os
import sys
import json
import requests
import urllib.parse
import time


def check_gcloud_auth():
    try:
        result = subprocess.run(["gcloud", "auth", "list"], capture_output=True, text=True)
        if "No credentialed accounts." in result.stdout:
            print("Error: Not authenticated with gcloud. Please run 'gcloud auth login' first.")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: Failed to check gcloud authentication status.")
        sys.exit(1)


def is_civitai_url(url: str):
    return url.startswith("https://civitai.com")


def civitai_url_with_token(url: str, civitai_api_token: str):
    if not is_civitai_url(url):
        return url

    if not civitai_api_token:
        return url

    return f"{url}?token={civitai_api_token}"


def is_huggingface_url(url: str):
    return url.startswith("https://huggingface.co")


def get_filename_from_huggingface_url(url: str):
    parsed_url = urllib.parse.urlparse(url)
    path_parts = parsed_url.path.split("/")

    if len(path_parts) < 5:
        raise ValueError(
            f"HuggingFace URL does not contain enough parts to extract filename: {url}"
        )

    filename = path_parts[-1]
    return filename


def get_filename_from_content_disposition(content_disposition):
    filename = None
    if "filename*" in content_disposition:
        filename_star = content_disposition.split("filename*=")[1].split(";")[0].strip()
        filename = urllib.parse.unquote(filename_star.split("''")[1])
    elif "filename" in content_disposition:
        filename = content_disposition.split("filename=")[1].split(";")[0].strip('"')

    return filename


def get_filename_from_url(url, civitai_api_token: str = None):
    if is_civitai_url(url):
        url = civitai_url_with_token(url, civitai_api_token)

    try:
        response = requests.head(url, allow_redirects=True)

        if "Content-Disposition" in response.headers:
            content_disposition = response.headers["Content-Disposition"]
            filename = get_filename_from_content_disposition(content_disposition)
        else:
            response = requests.get(
                url,
                headers={"Range": "bytes=0-1024"},
                stream=True,
                allow_redirects=True,
            )
            if "Content-Disposition" in response.headers:
                content_disposition = response.headers["Content-Disposition"]
                filename = get_filename_from_content_disposition(content_disposition)
            else:
                filename = url.split("/")[-1]

        if "." not in filename:
            print(f"No extension found for {filename}, assuming safetensors")
            filename += ".safetensors"

        return filename
    except Exception as e:
        print(f"Error: Failed to get filename from {url}: {e}")
        return None


def download_file(url, filename=None, civitai_api_token=None):
    start_time = time.time()
    if is_civitai_url(url):
        if not filename:
            filename = get_filename_from_url(url, civitai_api_token)
            filename = confirm_filename(filename)
        url = civitai_url_with_token(url, civitai_api_token)
        print(f"Downloading {url} to {filename}")
        try:
            result = subprocess.run(["pget", "-f", url, filename], timeout=600)
            if result.returncode != 0:
                raise RuntimeError(
                    "Download failed. You may need to pass in a valid CivitAI API token."
                )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Download failed due to timeout")
    elif is_huggingface_url(url):
        if not filename:
            filename = get_filename_from_huggingface_url(url)
            filename = confirm_filename(filename)
        print(f"Downloading from HuggingFace: {url} to {filename}")
        subprocess.run(["pget", "-f", url, filename])
    else:
        if not filename:
            filename = get_filename_from_url(url)
            filename = confirm_filename(filename)
        print(f"Downloading {url} to {filename}")
        subprocess.run(["pget", "-f", url, filename])

    print(f"Successfully downloaded {filename}")
    end_time = time.time()
    print(f"Downloaded in: {end_time - start_time:.2f} seconds")
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
    print(f"Uploaded to {destination_path}")


def upload_to_huggingface(local_file, subfolder):
    print(f"Uploading {local_file} to huggingface under {subfolder}")
    subprocess.run(
        [
            "huggingface-cli",
            "upload",
            "fofr/comfyui",
            local_file,
            f"{subfolder}/{local_file}",
        ]
    )
    print(f"Uploaded {local_file} to huggingface under {subfolder}")


def remove_files(*filenames):
    for filename in filenames:
        os.remove(filename)
        print(f"Deleted {filename}")


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
        "animatediff_models",
        "animatediff_motion_lora",
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


def confirm_filename(filename):
    while True:
        confirmed = input(f"Confirm filename {filename} (y/n): ").lower()
        if confirmed == "y":
            return filename
        elif confirmed == "n":
            new_filename = input("Enter new filename: ")
            return new_filename
        else:
            print("Invalid input. Please enter 'y' or 'n'.")


def process_file(
    url=None, filename=None, subfolder=None, no_hf=False, civitai_api_token=None
):
    if url:
        print(f"Processing {url}")
        local_file = download_file(url, filename, civitai_api_token)
    else:
        print(f"Processing {filename}")
        local_file = filename

    tarred_file = tar_file(local_file)
    upload_to_gcloud(tarred_file, "gs://replicate-weights/comfy-ui", subfolder)
    if not no_hf:
        upload_to_huggingface(local_file, subfolder)
    update_weights_json(subfolder, local_file)
    remove_files(local_file, tarred_file)
    subprocess.run(["python", "scripts/sort_weights.py"])


def process_weights_file(
    weights_file, subfolder=None, no_hf=False, civitai_api_token=None
):
    with open(weights_file, "r") as f:
        for line in f:
            url, filename = line.strip().split()
            process_file(url, filename, subfolder, no_hf, civitai_api_token)


def main():
    check_gcloud_auth()

    parser = argparse.ArgumentParser(
        description="Download a file, tar it, and upload to Google Cloud Storage and huggingface"
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
    parser.add_argument(
        "--no-hf",
        action="store_true",
        help="Do not upload to Hugging Face",
    )
    args = parser.parse_args()

    subfolder = get_subfolder()
    civitai_api_token = os.environ.get("CIVITAI_API_TOKEN")

    if args.weights_list:
        process_weights_file(
            args.weights_list, subfolder, args.no_hf, civitai_api_token
        )
    elif args.file:
        filename = args.filename if args.filename else None
        if args.file.startswith(("http://", "https://")):
            process_file(
                url=args.file,
                filename=filename,
                subfolder=subfolder,
                no_hf=args.no_hf,
                civitai_api_token=civitai_api_token,
            )
        elif os.path.isfile(args.file):
            process_file(
                filename=filename,
                subfolder=subfolder,
                no_hf=args.no_hf,
                civitai_api_token=civitai_api_token,
            )
        else:
            print(f"Error: The file or URL {args.file} is not valid.")
            sys.exit(1)


if __name__ == "__main__":
    main()
