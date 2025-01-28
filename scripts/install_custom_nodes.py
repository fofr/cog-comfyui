#!/usr/bin/env python3

import json
import os
import subprocess

"""
This script is used to clone specific versions of repositories.
It reads a JSON file containing repositories and their commit hashes, clones them into a specific directory,
and then checks out to the specified commit.
"""

json_file = "custom_nodes.json"
comfy_dir = "ComfyUI"
custom_nodes_dir = f"{comfy_dir}/custom_nodes/"

with open(json_file, "r") as file:
    repos = json.load(file)

# Loop over each repository in the list
for repo in repos:
    repo_url = repo["repo"]
    commit_hash = repo["commit"]
    repo_name = os.path.basename(repo_url.replace(".git", ""))

    # Check if the repository directory already exists
    repo_path = os.path.join(custom_nodes_dir, repo_name)
    if not os.path.isdir(repo_path):
        # Clone the repository into the destination directory
        print(
            f"Cloning {repo_url} into {repo_path} and checking out to commit {commit_hash}"
        )
        subprocess.run(["git", "clone", "--recursive", "-q", repo_url, repo_path])

        # Store the current directory and change to the repository's directory
        current_dir = os.getcwd()
        os.chdir(repo_path)
        subprocess.run(["git", "checkout", "-q", commit_hash])
        subprocess.run(["git", "submodule", "update", "--init", "--recursive", "-q"])

        # Change back to the original directory after operations
        os.chdir(current_dir)
    else:
        current_dir = os.getcwd()
        os.chdir(repo_path)

        current_commit = (
            subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        )
        print(f"Custom node installed for {repo_name} at {current_commit[:7]}")

        if current_commit[:7] != commit_hash[:7]:
            response = input(
                f"Do you want to update {repo_name}? Current ({current_commit[:7]}) is different from ({commit_hash[:7]}) (y/n): "
            )
            if response.lower() == "y":
                print(f"Checking out to commit {commit_hash}")
                subprocess.run(["git", "fetch", "-q"])
                subprocess.run(["git", "checkout", "-q", commit_hash])
                subprocess.run(["git", "submodule", "update", "--init", "--recursive", "-q"])
            else:
                print("Skipping checkout, keeping current commit")

        os.chdir(current_dir)

# Copy custom node config files to the correct directory
config_files = {
    "was_suite_config": {
        "src": "custom_node_configs/was_suite_config.json",
        "dest": os.path.join(custom_nodes_dir, "was-node-suite-comfyui/"),
    },
    "rgthree_config": {
        "src": "custom_node_configs/rgthree_config.json",
        "dest": os.path.join(custom_nodes_dir, "rgthree-comfy/"),
    },
    "comfy_settings": {
        "src": "custom_node_configs/comfy.settings.json",
        "dest": os.path.join(comfy_dir, "user", "default"),
    },
}

if "comfy_settings" in config_files:
    paths = config_files["comfy_settings"]
    if not os.path.exists(paths["dest"]):
        os.makedirs(paths["dest"])

for config_file, paths in config_files.items():
    if (
        os.path.isfile(paths["src"])
        and os.path.isdir(paths["dest"])
        and not os.path.exists(
            os.path.join(paths["dest"], os.path.basename(paths["src"]))
        )
    ):
        print(f"Copying {config_file} to {paths['dest']}")
        subprocess.run(["cp", paths["src"], paths["dest"]])
