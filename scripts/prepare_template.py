#!/usr/bin/env python3
import os
import shutil

FILES_TO_DELETE = [
    "examples",
    "test",
    "CHANGELOG.md",
    "supported_weights.md",
    "weights_licenses.md",
    "scripts/push_comfyui_manager_weights.py",
    "scripts/push_weights_from_hf.py",
    "scripts/push_weights.py",
    "scripts/sort_weights.py",
]

def prepare_template():
    """
    This script is used to prepare the template for a new model.
    It deletes unnecessary files and directories.
    It also overwrites the README.md with a blank file and header.
    Finally, it replaces predict.py with example_predict.py.
    """
    print("Preparing to clean up this template for a new model")
    print(
        "This will clear the README and delete the following files and directories:",
        "\n".join(FILES_TO_DELETE),
    )
    print("Are you sure you want to continue? (y/n)")

    if input() != "y":
        print("Aborting...")
        exit(1)

    print("Deleting unnecessary files and directories...")
    for file in FILES_TO_DELETE:
        if os.path.exists(file):
            if os.path.isdir(file):
                shutil.rmtree(file)
            else:
                os.remove(file)

    # Overwrite the README.md with a blank file and header "# Your repo"
    print("Overwriting README.md with a blank file and header")
    with open("README.md", "w") as f:
        f.write("# Your repo\n")

    print("Replacing predict.py with example_predict.py")
    shutil.move("example_predict.py", "predict.py")

prepare_template()
