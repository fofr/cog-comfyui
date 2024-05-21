import base64
import sys
import requests
import glob
import time


def check_if_cog_server_running():
    """
    To set up, first run a local cog server using:
       cog run -p 5000 python -m cog.server.http
    Then, in a separate terminal, generate samples
       python samples.py
    """
    try:
        response = requests.get("http://localhost:5000")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("cog server is not running. Start the server before running the tests.")
        print("cog run -p 5000 python -m cog.server.http")
        sys.exit(1)


def load_example_workflow_json(filename):
    with open(filename, "r") as file:
        return file.read()


def run(output_fn, **kwargs):
    if glob.glob(f"{output_fn.rsplit('.', 1)[0]}*"):
        print("Already ran", output_fn)
        return

    prediction_start = time.time()
    print("Running prediction", output_fn)
    url = "http://localhost:5000/predictions"
    response = requests.post(url, json={"input": kwargs})
    print(f"Prediction took: {time.time() - prediction_start:.2f}s")
    data = response.json()
    try:
        for i, datauri in enumerate(data["output"]):
            base64_encoded_data = datauri.split(",")[1]
            decoded_data = base64.b64decode(base64_encoded_data)
            filename = f"{output_fn.rsplit('.', 1)[0]}_{i}.{output_fn.rsplit('.', 1)[1]}"
            with open(
                filename, "wb"
            ) as f:
                f.write(decoded_data)
            print("Wrote", filename)
    except Exception as e:
        print("Error!", str(e))
        print("input:", kwargs)
        print(data["logs"])
        sys.exit(1)


def main():
    BASE_PATH = "examples/api_workflows"
    examples_to_test = [
        "anyline_api.json",
        "rembg_api.json",
        "pulid.json",
        "segment_anything_api.json",
        "layer_diffuse_api.json",
        "was_clipseg_basic_api.json",
        "comfyui_essentials_all_workflows.json",
        "bria_rmbg_api.json",
        "sd15_img2img.json",
        "sd15_txt2img.json",
        "sd15_inpainting.json",
        # "all_preprocessors.json",
    ]

    for example in examples_to_test:
        run(
            f"sample_{example.rsplit('.', 1)[0]}.webp",
            return_temp_files=True,
            workflow_json=load_example_workflow_json(f"{BASE_PATH}/{example}"),
        )


if __name__ == "__main__":
    check_if_cog_server_running()
    main()
