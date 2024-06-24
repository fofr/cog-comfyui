import tarfile
import os
import subprocess
import requests
import urllib.parse
import shutil
import json
import time

from cog import BaseModel, Input, Path, Secret
from huggingface_hub import hf_hub_download

os.environ["DOWNLOAD_LATEST_WEIGHTS_MANIFEST"] = "true"
os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"

HF_TEMP_DIR = "TEMP_HF"
USER_MODELS_DIR = "user_models"


def is_civitai_url(url: str):
    return url.startswith("https://civitai.com")


def civitai_url_with_token(url: str, civitai_api_token: Secret):
    if not is_civitai_url(url):
        return url

    if not civitai_api_token:
        return url

    return f"{url}?token={civitai_api_token.get_secret_value()}"


def is_huggingface_url(url: str):
    return url.startswith("https://huggingface.co")


def extract_parts_from_huggingface_url(url: str):
    # HUGGINGFACE_CO_URL_TEMPLATE
    # https://huggingface.co/{repo_id}/resolve/{revision}/{filename}

    parsed_url = urllib.parse.urlparse(url)
    path_parts = parsed_url.path.split("/")

    if len(path_parts) < 5:
        raise ValueError(
            f"HuggingFace URL does not contain enough parts to extract all required parts: {url}"
        )

    repo_id = f"{path_parts[1]}/{path_parts[2]}"
    revision = path_parts[4]
    filename_and_path = path_parts[5:]
    filename = filename_and_path[-1]

    return repo_id, revision, filename_and_path, filename


def get_filename_from_content_disposition(content_disposition):
    filename = None
    if "filename*" in content_disposition:
        # Extract and decode the filename* parameter
        filename_star = content_disposition.split("filename*=")[1].split(";")[0].strip()
        filename = urllib.parse.unquote(filename_star.split("''")[1])
    elif "filename" in content_disposition:
        # Extract the filename parameter
        filename = content_disposition.split("filename=")[1].split(";")[0].strip('"')

    return filename


def get_filename_from_url(url, civitai_api_token: Secret = None):
    if is_civitai_url(url):
        url = civitai_url_with_token(url, civitai_api_token)

    try:
        # First try with HEAD request
        response = requests.head(url, allow_redirects=True)

        # Check if the response contains the Content-Disposition header
        if "Content-Disposition" in response.headers:
            content_disposition = response.headers["Content-Disposition"]
            filename = get_filename_from_content_disposition(content_disposition)
        else:
            # If HEAD request fails to get filename, fall back to partial GET request
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
                # Fallback to the last part of the URL if no Content-Disposition header is present
                filename = url.split("/")[-1]

        if "." not in filename:
            print(f"No extension found for {filename}, assuming safetensors")
            filename += ".safetensors"

        print("civitai filename:", filename)
        return filename
    except Exception as e:
        return str(e)


def download_from_civitai(
    url: str,
    filename: str = "checkpoint.safetensors",
    civitai_api_token: Secret = None,
):
    print(f"Downloading {url} to {filename}")
    url = civitai_url_with_token(url, civitai_api_token)

    start_time = time.time()
    try:
        result = subprocess.run(["pget", "-f", url, filename], timeout=600)
        if result.returncode != 0:
            raise RuntimeError(
                "Download failed. You need to pass in a valid CivitAI API token if the download showed a 401 Unauthorized error. You can create an API key from the bottom of https://civitai.com/user/account"
            )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Download failed due to timeout")

    print(f"Successfully downloaded {filename}")
    end_time = time.time()
    print(f"Downloaded in: {end_time - start_time:.2f} seconds")
    return filename


def download_from_huggingface(
    url: str,
    file_type: str = "CHECKPOINTS",
    huggingface_read_token: Secret = None,
):
    repo_id, revision, filename_and_path, filename = extract_parts_from_huggingface_url(
        url
    )

    start_time = time.time()
    print("Downloading from HuggingFace:")
    print("url:", url)
    print("repo_id:", repo_id)
    print("revision:", revision)
    print("filename_and_path:", "/".join(filename_and_path))
    print("filename:", filename)

    token = (
        huggingface_read_token.get_secret_value() if huggingface_read_token else False
    )
    hf_hub_download(
        repo_id=repo_id,
        revision=revision,
        filename="/".join(filename_and_path),
        local_dir=HF_TEMP_DIR,
        token=token,
    )

    # Move the downloaded file from HF_TEMP_DIR to the appropriate directory
    src_path = os.path.join(HF_TEMP_DIR, "/".join(filename_and_path))
    dest_dir = os.path.join(USER_MODELS_DIR, file_type.lower())
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)
    shutil.move(src_path, dest_path)

    print(f"Successfully downloaded {filename}")
    end_time = time.time()
    print(f"Downloaded in: {end_time - start_time:.2f} seconds")

    return filename


def clean_directories():
    for dir in [HF_TEMP_DIR, USER_MODELS_DIR]:
        dir = Path(dir)
        if dir.exists() and dir.is_dir():
            shutil.rmtree(dir)


class TrainingOutput(BaseModel):
    weights: Path


def train(
    checkpoints: str = Input(
        description="A list of HuggingFace or CivitAI download URLs (use line breaks to upload multiples)",
        default=None,
    ),
    loras: str = Input(
        description="A list of HuggingFace or CivitAI download URLs (use line breaks to upload multiples)",
        default=None,
    ),
    upscale_models: str = Input(
        description="A list of HuggingFace or CivitAI download URLs (use line breaks to upload multiples)",
        default=None,
    ),
    embedding_models: str = Input(
        description="A list of HuggingFace or CivitAI download URLs (use line breaks to upload multiples)",
        default=None,
    ),
    controlnets: str = Input(
        description="A list of HuggingFace or CivitAI download URLs (use line breaks to upload multiples)",
        default=None,
    ),
    animatediff_models: str = Input(
        description="A list of HuggingFace or CivitAI download URLs (use line breaks to upload multiples)",
        default=None,
    ),
    animatediff_loras: str = Input(
        description="A list of HuggingFace or CivitAI download URLs (use line breaks to upload multiples)",
        default=None,
    ),
    huggingface_read_token: Secret = Input(
        description="Optional: Your HuggingFace read token. Only needed if you are trying to download HuggingFace weights that require authentication. You can create or get a read token from https://huggingface.co/settings/tokens",
        default=None,
    ),
    civitai_api_token: Secret = Input(
        description="Optional: Your CivitAI API token. Only needed if you are trying to download CivitAI weights that require authentication. You can create an API key from the bottom of https://civitai.com/user/account",
        default=None,
    ),
) -> TrainingOutput:
    clean_directories()

    lists_of_urls = {
        "CHECKPOINTS": checkpoints.splitlines() if checkpoints else [],
        "LORAS": loras.splitlines() if loras else [],
        "UPSCALE_MODELS": upscale_models.splitlines() if upscale_models else [],
        "EMBEDDINGS": embedding_models.splitlines() if embedding_models else [],
        "CONTROLNETS": controlnets.splitlines() if controlnets else [],
        "ANIMATEDIFF_MODELS": animatediff_models.splitlines()
        if animatediff_models
        else [],
        "ANIMATEDIFF_LORAS": animatediff_loras.splitlines()
        if animatediff_loras
        else [],
    }
    lists_of_urls = {
        k: [url.strip() for url in v] for k, v in lists_of_urls.items() if v
    }

    filenames = {}

    for file_type, urls in lists_of_urls.items():
        filenames[file_type] = []
        for url in urls:
            if not (is_huggingface_url(url) or is_civitai_url(url)):
                raise ValueError("URL must be from 'huggingface.co' or 'civitai.com'")

            if is_civitai_url(url):
                filename = get_filename_from_url(url, civitai_api_token)
                download_from_civitai(
                    url,
                    filename=f"{USER_MODELS_DIR}/{file_type.lower()}/{filename}",
                    civitai_api_token=civitai_api_token,
                )
                filenames[file_type].append(filename)
            elif is_huggingface_url(url):
                filename = download_from_huggingface(
                    url,
                    file_type=file_type,
                    huggingface_read_token=huggingface_read_token,
                )
                filenames[file_type].append(filename)

    try:
        weights_json_path = os.path.join(USER_MODELS_DIR, "weights.json")
        with open(weights_json_path, "w") as json_file:
            json.dump(filenames, json_file, indent=2)
    except Exception as e:
        raise RuntimeError(
            f"No files were downloaded. Could not write weights.json: {e}"
        )

    # Create a tar file of the weights
    tar_file_path = "weights.tar"
    with tarfile.open(tar_file_path, "w") as tar:
        # Add the user_models directory to the tar file
        user_models_dir = Path(USER_MODELS_DIR)
        if user_models_dir.exists() and user_models_dir.is_dir():
            for root, _, files in os.walk(user_models_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    tar.add(
                        file_path, arcname=os.path.relpath(file_path, user_models_dir)
                    )
                    print(f"Added {file_path} to tar file.")

    tar_file_size = os.path.getsize(tar_file_path) / (1024 * 1024)  # size in MB
    print(f"Size of the tar file: {tar_file_size:.2f} MB")

    if tar_file_size > 9000:
        print("If weights are larger than ~10GB, you may find that uploads will fail.")

    clean_directories()

    print("====================================")
    print("When using your new model, use these filenames in your JSON workflow:")
    for file_type, files in filenames.items():
        for filename in files:
            print(filename)

    return TrainingOutput(weights=Path("weights.tar"))
