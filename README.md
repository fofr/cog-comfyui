# cog-comfyui

Run ComfyUI workflows on Replicate:
https://replicate.com/fofr/comfyui

It is ideal for using a ComfyUI workflow with a production ready API. And it's ideal for using with deployments.

We recommend:

- try it with your favorite workflow and make sure it works
- write code to customise the JSON you pass to the model, for example changing seeds or prompts
- use the Replicate API to run the workflow

## What’s included

We've tried to include many of the most popular model weights:
[View list of supported weights](https://github.com/fofr/cog-comfyui/blob/main/supported_weights.md)

The following custom nodes are also supported, these are fixed to specific commits:

- [ComfyUI IPAdapter Plus](https://github.com/cubiq/ComfyUI_IPAdapter_plus/tree/4e898fe)
- [ComfyUI Controlnet Aux](https://github.com/Fannovel16/comfyui_controlnet_aux/tree/6d6f63c)
- [ComfyUI Inspire Pack](https://github.com/ltdrdata/ComfyUI-Inspire-Pack/tree/c8231dd)
- [ComfyUI Logic](https://github.com/theUpsider/ComfyUI-Logic/tree/fb88973)
- [ComfyUI AnimateDiff Evolved](https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved/tree/d2bf367)

Raise an issue to request more custom nodes or models, or use this model as a template to roll your own.

## How to use

### 1. Get your API JSON

You’ll need the API version of your ComfyUI workflow. This is different to the commonly shared JSON version, it does not included visual information about nodes, etc.

To get your API JSON:

1. Turn on the "Enable Dev mode Options" from the ComfyUI settings (via the settings icon)
2. Load your workflow into ComfyUI
3. Export your API JSON using the "Save (API format)" button

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

Run the [following script](https://github.com/fofr/cog-comfyui/blob/main/scripts/clone_plugins.sh) to install all the custom nodes:

```sh
./scripts/clone_plugins.sh
```

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
