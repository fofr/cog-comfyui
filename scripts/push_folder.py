#!/usr/bin/env python
import argparse
import subprocess
import os
import sys
import shutil
import json
from datetime import datetime
from pathlib import Path

def copy_to_temp(source_path):
    folder_name = os.path.basename(source_path)
    temp_path = os.path.join('temp', folder_name)
    os.makedirs('temp', exist_ok=True)

    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)

    # Copy the contents
    shutil.copytree(source_path, temp_path)

    return temp_path

def create_tar(folder_path):
    original_dir = os.getcwd()
    folder_name = os.path.basename(folder_path)
    tar_name = f"{folder_name}.tar"

    try:
        # Change to the parent directory of the folder
        os.chdir(os.path.dirname(folder_path))

        # Create tar file
        subprocess.run(["tar", "-cvf", tar_name, folder_name])

        # Move tar file to original directory
        shutil.move(tar_name, os.path.join(original_dir, tar_name))

    finally:
        # Change back to original directory
        os.chdir(original_dir)

    return tar_name

def upload_to_gcloud(local_file, destination_blob_name, subfolder):
    destination_path = f"{destination_blob_name}/{subfolder}/{local_file}"
    print(f"Uploading {local_file} to {destination_path}")
    subprocess.run(["gcloud", "storage", "cp", local_file, destination_path])
    print(f"Uploaded to {destination_path}")

def update_weights_json(subfolder, folder_name):
    subfolder = subfolder.upper()
    with open("weights.json", "r+") as f:
        weights_data = json.load(f)
        if subfolder in weights_data:
            if folder_name not in weights_data[subfolder]:
                weights_data[subfolder].append(folder_name)
                f.seek(0)
                json.dump(weights_data, f, indent=4)
                f.truncate()
                print(f"Added {folder_name} to {subfolder} in weights.json")
                update_changelog(subfolder, folder_name)
            else:
                print(f"{folder_name} already exists in {subfolder} in weights.json")
        else:
            print(f"{subfolder} not found in weights.json")

def update_changelog(subfolder, folder_name):
    changelog_file = "CHANGELOG.md"
    today = datetime.now().strftime("%Y-%m-%d")
    update_line = f"- Add {folder_name} to {subfolder.lower()}\n"

    try:
        with open(changelog_file, "r+") as file:
            content = file.readlines()
            if content[0].strip() != f"## {today}":
                content.insert(0, f"\n## {today}\n\n")

            # Find the index of the current day's section
            today_index = next(
                (i for i, line in enumerate(content) if line.strip() == f"## {today}"),
                None,
            )

            if today_index is not None:
                # Insert the update line right after the current day's header
                content.insert(today_index + 1, update_line)
            else:
                # If today's section wasn't found, append to the top
                content.insert(2, update_line)

            file.seek(0)
            file.writelines(content)
    except FileNotFoundError:
        print(f"Warning: Changelog file '{changelog_file}' not found. Skipping changelog update.")
    except IOError as e:
        print(f"Error updating changelog: {e}")

def cleanup(temp_path, tar_file):
    # Remove temporary directory and tar file
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        print(f"Cleaned up temporary directory: {temp_path}")

    if os.path.exists(tar_file):
        os.remove(tar_file)
        print(f"Cleaned up tar file: {tar_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Process a folder, tar it, and upload to Google Cloud Storage"
    )
    parser.add_argument(
        "folder_path",
        help="Path to the folder to process (e.g., ComfyUI/models/LLM/Florence-2-large-PromptGen-v2.0)"
    )
    args = parser.parse_args()

    # Extract subfolder from path (e.g., 'LLM' from the path)
    path_parts = Path(args.folder_path).parts
    models_index = path_parts.index('models')
    if models_index + 1 >= len(path_parts):
        print("Error: Invalid path structure. Expected path like 'ComfyUI/models/SUBFOLDER/FOLDERNAME'")
        sys.exit(1)

    subfolder = path_parts[models_index + 1]
    folder_name = path_parts[-1]

    # Process the folder
    try:
        # Copy to temp
        temp_path = copy_to_temp(args.folder_path)
        print(f"Copied contents to: {temp_path}")

        # Create tar
        tar_file = create_tar(temp_path)
        print(f"Created tar file: {tar_file}")

        # Upload to Google Cloud
        upload_to_gcloud(tar_file, "gs://replicate-weights/comfy-ui", subfolder)

        # Update changelog and weights.json
        update_weights_json(subfolder, folder_name)
        subprocess.run(["python", "scripts/sort_weights.py"])

    finally:
        # Cleanup
        cleanup(temp_path, tar_file)

if __name__ == "__main__":
    main()
