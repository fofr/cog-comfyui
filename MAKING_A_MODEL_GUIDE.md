# Adapting this template for your model

This guide will help you adapt the `cog-comfyui` template repository for your own model.

If you haven’t used `cog` before or pushed a Replicate model, these are good starting guides:

- https://cog.run/getting-started-own-model
- https://replicate.com/docs/guides/push-a-model


## Create a new repo from the template

Use https://github.com/fofr/cog-comfyui as a template to create a new repository

## Prepare the template

After you have git cloned your new repository locally, including submodules, you should run the `prepare_template.py` script.

This will:

- delete unnecessary files and directories.
- overwrite the `README.md` with a blank file and header.
- replace `predict.py` with `example_predict.py`

Run this script:

```sh
python scripts/prepare_template.py
```

Check what has been deleted and replaced before committing:

```sh
git status
git diff
```

## Add your workflow

You should save the API version of your workflow as `workflow_api.json`.

It also helps to keep a copy of the UI version too, as `workflow_ui.json`.

## Update the inputs to your model

`predict.py` is the entrypoint to your model. You can read about `predict.py` and the inputs you can use in the [Cog documentation](https://cog.run/python/#predictorpredictkwargs).

You'll end up with something like this:

```python
def predict(
        self,
        prompt: str = Input(
            default="",
        ),
        negative_prompt: str = Input(
            description="Things you do not want to see in your image",
            default="",
        ),
        image: Path = Input(
            description="An input image",
            default=None,
        ),
        ...
    ) -> List[Path]:
        """Run a single prediction on the model"""
        ...
```

To make sure these inputs carry over to the workflow, you'll need to update the JSON object with new values. `example_predict.py` includes an example of this:

Within the predict method:

```python
self.update_workflow(
    workflow,
    prompt=prompt,
    negative_prompt=negative_prompt,
    seed=seed,
)
```

And in the `update_workflow` method (in the Predictor class):

```python
def update_workflow(self, workflow, **kwargs):
  # The node
  positive_prompt = workflow["6"]["inputs"]

  # Updating one of the nodes inputs
  positive_prompt["text"] = kwargs["prompt"]

  negative_prompt = workflow["7"]["inputs"]
  negative_prompt["text"] = f"nsfw, {kwargs['negative_prompt']}"

  sampler = workflow["3"]["inputs"]
  sampler["seed"] = kwargs["seed"]
```

## Remove any custom nodes you do not need

To remove a custom node you should:

- remove its corresponding entry from the `custom_nodes.json` file
- optional: delete any corresponding helpers in `custom_node_helpers`
- optional: delete any configs from `custom_nodes_configs`
- optional: delete dependencies from `cog.yaml`

If you've already installed the nodes, make sure to also remove it from the `ComfyUI/custom_nodes` directory.

## Add your own custom nodes

The simplest way to add new nodes is to:

- add a new entry to the `custom_nodes.json` file, with the repo URL and the commit hash you want to use (usually the latest)
- add any dependencies from the custom node’s `requirements.txt` to the `cog.yaml` file (if they are not already there)
- rerun `scripts/install_custom_nodes.py` to install the new nodes

Some nodes will try to download weights on demand. You might want to avoid doing this from your Replicate model. The easiest fix is to make sure the downloaded weights are also pushed with your container. If you choose to do this, make sure to also update `.dockerignore`, which by default excludes weight from the container.

## Running the model locally

You can run the model with defaults via cog:

```sh
cog predict
```

Or if you want to pass inputs:

```sh
cog predict -i prompt="something" -i image=@/path/to/image.jpg
```

## Deploying your model to Replicate

Create a new model from https://replicate.com/create

Push your cog container to Replicate:

```sh
cog push r8.im/<username>/<model-name>
```
