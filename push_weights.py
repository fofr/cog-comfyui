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
    confirm_step(f"About to download file from {url} to {filename}")
    subprocess.run(["wget", url, "-O", filename])
    print(f"Successfully downloaded {filename}")
    return filename


def tar_file(filename):
    tar_filename = filename.split(".")[0] + ".tar"
    confirm_step(f"About to tar file {filename} and save as {tar_filename}")
    subprocess.run(["tar", "-cvf", tar_filename, filename])
    print(f"Successfully tarred {filename} to {tar_filename}")
    return tar_filename


def upload_to_gcloud(local_file, destination_blob_name):
    confirm_step(f"About to upload {local_file} to {destination_blob_name}")
    subprocess.run(["gcloud", "storage", "cp", local_file, destination_blob_name])
    print(f"Successfully uploaded to {destination_blob_name}")


def remove_files(*filenames):
    confirm_step(f"About to remove the following files: {', '.join(filenames)}")
    for filename in filenames:
        os.remove(filename)
        print(f"Successfully removed {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Download a file, tar it, and upload to Google Cloud Storage"
    )
    parser.add_argument("url", help="The URL of the file to download")
    parser.add_argument(
        "--filename",
        help="The local filename to save the file as. Defaults to the filename in the URL",
    )
    args = parser.parse_args()

    local_file = download_file(args.url, args.filename)
    tarred_file = tar_file(local_file)
    upload_to_gcloud(tarred_file, "gs://replicate-weights/comfy-ui/" + tarred_file)
    remove_files(local_file, tarred_file)


if __name__ == "__main__":
    main()
