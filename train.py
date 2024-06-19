import tarfile
import os
import subprocess
import requests
import urllib.parse
import shutil
import json

from typing import List
from cog import BaseModel, Input, Path, Secret

os.environ["DOWNLOAD_LATEST_WEIGHTS_MANIFEST"] = "true"


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


def get_filename_from_url(url):
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

        # print(f"Filename for {url}: {filename}")
        return filename
    except Exception as e:
        return str(e)


def download_file(
    url: str, filename: str = "checkpoint.safetensors", civitai_api_token: Secret = None
):
    is_civitai = url.startswith("https://civitai.com")
    is_huggingface = url.startswith("https://huggingface.co")

    if not (is_huggingface or is_civitai):
        raise ValueError("URL must be from 'huggingface.co' or 'civitai.com'")

    if civitai_api_token and is_civitai:
        print(f"Downloading {url} to {filename}")

        # https://developer.civitai.com/docs/api/public-rest#get-apiv1models
        url = f"{url}?token={civitai_api_token.get_secret_value()}"
    else:
        print(f"Downloading {url} to {filename}")

    subprocess.run(["pget", "--log-level", "warn", "-f", url, filename], timeout=120)

    print(f"Successfully downloaded {filename}")
    return filename


def clean_user_models_dir(dir: str):
    user_models_dir = Path(dir)
    if user_models_dir.exists() and user_models_dir.is_dir():
        shutil.rmtree(user_models_dir)


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
    civitai_api_token: Secret = Input(
        description="Optional: Your CivitAI API token. Only needed if you are needing to download CivitAI weights that require authentication. You can create an API key from the bottom of https://civitai.com/user/account",
        default=None,
    ),
) -> TrainingOutput:
    user_models_directory_name = "user_models"
    clean_user_models_dir(user_models_directory_name)

    lists_of_files = {
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
    lists_of_files = {
        k: [file.strip() for file in v] for k, v in lists_of_files.items() if v
    }

    filenames = {}

    for file_type, files in lists_of_files.items():
        filenames[file_type] = []
        for file in files:
            if file.startswith("https://"):
                filename = get_filename_from_url(file)
                file = download_file(
                    file,
                    filename=f"{user_models_directory_name}/{file_type.lower()}/{filename}",
                    civitai_api_token=civitai_api_token,
                )
                filenames[file_type].append(filename)

    weights_json_path = os.path.join(user_models_directory_name, "weights.json")
    with open(weights_json_path, "w") as json_file:
        json.dump(filenames, json_file, indent=2)

    # Create a tar file of the weights
    with tarfile.open("weights.tar", "w") as tar:
        # Add the user_models directory to the tar file
        user_models_dir = Path(user_models_directory_name)
        if user_models_dir.exists() and user_models_dir.is_dir():
            for root, _, files in os.walk(user_models_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    tar.add(
                        file_path, arcname=os.path.relpath(file_path, user_models_dir)
                    )
                    print(f"Added {file_path} to tar file.")

    # Remove user_models directory
    clean_user_models_dir(user_models_directory_name)

    print("====================================")
    print("When using your new model, use these filenames in your JSON workflow:")
    for file_type, files in filenames.items():
        for filename in files:
            print(filename)

    return TrainingOutput(weights=Path("weights.tar"))
