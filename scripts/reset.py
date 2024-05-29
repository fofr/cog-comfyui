#!/usr/bin/env python3
import subprocess

"""
This script is used to reset the ComfyUI environment.
It deletes the ComfyUI directory before reinstalling ComfyUI and every custom node.
"""

print("Preparing to reset the ComfyUI environment...")
print(
    "This will delete the ComfyUI directory before reinstalling ComfyUI and every custom node."
)
print("Are you sure you want to continue? (y/n)")

if input() != "y":
    print("Aborting...")
    exit(1)

print("Deleting the ComfyUI directory...")
subprocess.run(["sudo", "rm", "-rf", "ComfyUI"])

print("Installing ComfyUI...")
subprocess.run(["git", "submodule", "update", "--init", "--recursive"])

print("Installing custom nodes...")
subprocess.run(["./scripts/install_custom_nodes.py"])
print("Custom nodes installed successfully.")
