#!/usr/bin/env python3

import os
import subprocess
from datetime import datetime

"""
This script checks for updates to ComfyUI.
It fetches the latest commit on the main branch,
prompts the user if they want to update, and updates if confirmed.
"""

comfy_dir = "ComfyUI"
changelog_file = "CHANGELOG.md"
gitmodules_file = ".gitmodules"


def get_latest_commit(repo_path):
    try:
        subprocess.run(
            ["git", "fetch", "origin", "master"],
            cwd=repo_path,
            check=True,
            capture_output=True,
        )
        result = subprocess.run(
            ["git", "rev-parse", "origin/master"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Failed to fetch latest commit for {repo_path}")
        return None


def get_current_commit(repo_path):
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(f"Failed to get current commit for {repo_path}")
        return None


def update_gitmodules(new_commit):
    try:
        with open(gitmodules_file, "r") as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if line.strip().startswith("commit ="):
                lines[i] = f"\tcommit = {new_commit}\n"

        with open(gitmodules_file, "w") as file:
            file.writelines(lines)
    except FileNotFoundError:
        print(f"Warning: .gitmodules file '{gitmodules_file}' not found.")
    except IOError as e:
        print(f"Error updating .gitmodules: {e}")


def update_changelog(compare_url):
    today = datetime.now().strftime("%Y-%m-%d")
    update_line = f"- [Update ComfyUI to latest]({compare_url})\n"

    try:
        with open(changelog_file, "r+") as file:
            content = file.readlines()

            while content and not content[0].strip():
                content.pop(0)

            if content[0].strip() != f"## {today}":
                content.insert(0, f"## {today}\n\n")

            # Find the index of the current day's section
            today_index = next(
                (i for i, line in enumerate(content) if line.strip() == f"## {today}"),
                None,
            )

            if today_index is not None:
                # Insert the update line right after the current day's header
                content.insert(today_index + 1, update_line)
            else:
                # If today's section wasn't found (which shouldn't happen), append to the top
                content.insert(2, update_line)

            file.seek(0)
            file.writelines(content)
    except FileNotFoundError:
        print(
            f"Warning: Changelog file '{changelog_file}' not found. Skipping changelog update."
        )
    except IOError as e:
        print(f"Error updating changelog: {e}")


print("\nChecking ComfyUI...")

# Check if ComfyUI directory exists
if not os.path.isdir(comfy_dir):
    print("ComfyUI directory not found. Skipping.")
    exit(1)

# Get the latest and current commits
latest_commit = get_latest_commit(comfy_dir)
current_commit = get_current_commit(comfy_dir)

if latest_commit is None or current_commit is None:
    print("Failed to fetch commits. Skipping.")
    exit(1)

if latest_commit[:7] != current_commit[:7]:
    print("Update available for ComfyUI")
    print(f"Current commit: {current_commit[:7]}")
    print(f"Latest commit: {latest_commit[:7]}")

    # Generate GitHub comparison URL
    compare_url = f"https://github.com/comfyanonymous/ComfyUI/compare/{current_commit[:7]}...{latest_commit[:7]}"
    print(f"Comparison URL: {compare_url}")

    response = input("Do you want to update? (y/n): ")
    if response.lower() == "y":
        print("Updating ComfyUI...")
        subprocess.run(["git", "checkout", latest_commit], cwd=comfy_dir, check=True)
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=comfy_dir,
            check=True,
        )

        update_changelog(compare_url)
        update_gitmodules(latest_commit)

        print(f"Updated ComfyUI to {latest_commit[:7]}")
    else:
        print("Skipping update for ComfyUI")
else:
    print("ComfyUI is up to date")

print("\nFinished checking for updates. CHANGELOG.md and .gitmodules have been updated if necessary.")
