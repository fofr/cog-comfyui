# cog-comfyui

Run ComfyUI workflows on Replicate:

https://replicate.com/fofr/any-comfyui-workflow

We recommend:

- trying it with your favorite workflow and make sure it works
- writing code to customise the JSON you pass to the model, for example changing seeds or prompts
- using the Replicate API to run the workflow

TLDR: json blob -> img/mp4

## What’s included

We've tried to include many of the most popular model weights and custom nodes:

- [View list of supported weights](https://github.com/fofr/cog-comfyui/blob/main/supported_weights.md)
- [View list of supported custom nodes](https://github.com/fofr/cog-comfyui/blob/main/custom_nodes.json)

Raise an issue to request more custom nodes or models, or use this model as a template to roll your own.

## Examples of models derived from this one

See the commits on these repositories to see how to convert this repo into a new Replicate model:

- https://github.com/fofr/cog-face-to-many
- https://github.com/fofr/cog-video-morpher
- https://github.com/fofr/cog-stickers
- https://github.com/fofr/cog-material-transfer

## How to use

### 1. Get your API JSON

You’ll need the API version of your ComfyUI workflow. This is different to the commonly shared JSON version, it does not included visual information about nodes, etc.

To get your API JSON:

1. Turn on the "Enable Dev mode Options" from the ComfyUI settings (via the settings icon)
2. Load your workflow into ComfyUI
3. Export your API JSON using the "Save (API format)" button

https://private-user-images.githubusercontent.com/319055/298630636-e3af1b59-ddd8-426c-a833-808e7f199fac.mp4

### 2. Gather your input files

If your model takes inputs, like images for img2img or controlnet, you have 3 options:

#### Use a URL

Modify your API JSON file to point at a URL:

```diff
- "image": "/your-path-to/image.jpg",
+ "image": "https://example.com/image.jpg",
```

#### Upload a single input

You can also upload a single input file when running the model.

This file will be saved as `input.[extension]` – for example `input.jpg`. It'll be placed in the ComfyUI `input` directory, so you can reference in your workflow with:

```diff
- "image": "/your-path-to/image.jpg",
+ "image": "image.jpg",
```

#### Upload a zip file or tar file of your inputs

These will be downloaded and extracted to the `input` directory. You can then reference them in your workflow based on their relative paths.

So a zip file containing:

```
- my_img.png
- references/my_reference_01.jpg
- references/my_reference_02.jpg
```

Might be used in the workflow like:

```
"image": "my_img.png",
...
"directory": "references",
```

### Run your workflow

With all your inputs updated, you can now run your workflow.

Some workflows save temporary files, for example pre-processed controlnet images. You can also return these by enabling the `return_temp_files` option.

## Developing locally

Clone this repository:

```sh
git clone --recurse-submodules https://github.com/fofr/cog-comfyui.git
```

Run the [following script](https://github.com/fofr/cog-comfyui/blob/main/scripts/install_custom_nodes.py) to install all the custom nodes:

```sh
./scripts/install_custom_nodes.py
```

You can view the list of nodes in [custom_nodes.json](https://github.com/fofr/cog-comfyui/blob/main/custom_nodes.json)

### Running the Web UI from your Cog container

1. **GPU Machine**: Start the Cog container and expose port 8188:
```sh
sudo cog run -p 8188 bash
```
Running this command starts up the Cog container and let's you access it

2. **Inside Cog Container**: Now that we have access to the Cog container, we start the server, binding to all network interfaces:
```sh
cd ComfyUI/
python main.py --listen 0.0.0.0
```

3. **Local Machine**: Access the server using the GPU machine's IP and the exposed port (8188):
`http://<gpu-machines-ip>:8188`

When you goto `http://<gpu-machines-ip>:8188` you'll see the classic ComfyUI web form!
