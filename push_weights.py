import argparse
import subprocess
import os


def confirm_step(message):
    print(message)
    input("Press Enter to continue...")


def download_file(url, filename=None):
    if not filename:
        filename = url.split("/")[-1]
        filename = filename.rstrip("?download=true")
    # confirm_step(f"About to download file from {url} to {filename}")
    print(f"Downloading {url} to {filename}")
    subprocess.run(["wget", url, "-O", filename])
    print(f"Successfully downloaded {filename}")
    return filename


def tar_file(filename):
    tar_filename = filename + ".tar"
    subprocess.run(["tar", "-cvf", tar_filename, filename])
    print(f"Tarred {filename} to {tar_filename}")
    return tar_filename


def upload_to_gcloud(local_file, destination_blob_name, subfolder):
    # confirm_step(f"About to upload {local_file} to {destination_blob_name}/{subfolder}/{local_file}")
    print(f"Uploading {local_file} to {destination_blob_name}/{subfolder}/{local_file}")
    subprocess.run(
        ["gcloud", "storage", "cp", local_file, f"{destination_blob_name}/{subfolder}/{local_file}"]
    )
    print(f"Successfully uploaded to {destination_blob_name}")


def remove_files(*filenames):
    # confirm_step(f"About to remove the following files: {', '.join(filenames)}")
    print(f"About to remove the following files: {', '.join(filenames)}")
    for filename in filenames:
        os.remove(filename)
        print(f"Successfully removed {filename}")


def get_subfolder():
    subfolders = [
        "checkpoints",
        "upscale_models",
        "controlnet",
        "clip_vision",
        "loras",
        "ipadapter",
        "onnx",
        "vae",
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


def process_file(url, filename=None):
    local_file = download_file(url, filename)
    tarred_file = tar_file(local_file)
    subfolder = get_subfolder()
    upload_to_gcloud(tarred_file, "gs://replicate-weights/comfy-ui", subfolder)
    remove_files(local_file, tarred_file)


def process_weights_file(weights_file):
    with open(weights_file, 'r') as f:
        for line in f:
            url, filename = line.strip().split()
            process_file(url, filename)


def main():
    parser = argparse.ArgumentParser(
        description="Download a file, tar it, and upload to Google Cloud Storage"
    )
    parser.add_argument("--file", help="The weights file with URLs to download")
    parser.add_argument("--url", help="The URL of the file to download")
    parser.add_argument(
        "--filename",
        help="The local filename to save the file as. Defaults to the filename in the URL",
    )
    args = parser.parse_args()

    if args.file:
        process_weights_file(args.file)
    elif args.url:
        process_file(args.url, args.filename)


if __name__ == "__main__":
    main()
