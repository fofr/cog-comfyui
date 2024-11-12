#!/usr/bin/env python3

import json
import os
import subprocess
from datetime import datetime

"""
This script checks for updates to custom node repositories.
It fetches the latest commit on the main branch for each repo,
prompts the user if they want to update, and updates the JSON file and repo if confirmed.
"""

json_file = "custom_nodes.json"
comfy_dir = "ComfyUI"
custom_nodes_dir = f"{comfy_dir}/custom_nodes/"
changelog_file = "CHANGELOG.md"


def get_latest_commit(repo_path):
    def try_branch(branch):
        try:
            subprocess.run(
                ["git", "fetch", "origin", branch],
                cwd=repo_path,
                check=True,
                capture_output=True,
            )
            result = subprocess.run(
                ["git", "rev-parse", f"origin/{branch}"],
                cwd=repo_path,
                check=True,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None

    try:
        # Try main branch first, fall back to master
        for branch in ["main", "master"]:
            commit = try_branch(branch)
            if commit:
                return commit

        print(f"Failed to fetch latest commit for {repo_path}")
        return None

    except subprocess.CalledProcessError:
        print(f"Failed to fetch latest commit for {repo_path}")
        return None


def update_json_file(repos):
    with open(json_file, "w") as file:
        json.dump(repos, file, indent=2)
        file.write("\n")


def update_changelog(repo_name, compare_url):
    today = datetime.now().strftime("%Y-%m-%d")
    update_line = f"- [Updated {repo_name}]({compare_url})\n"

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


with open(json_file, "r") as file:
    repos = json.load(file)

# Loop over each repository in the list
for repo in repos:
    repo_url = repo["repo"]
    current_commit = repo["commit"]
    repo_name = os.path.basename(repo_url.replace(".git", ""))

    print(f"\nChecking {repo_name}...")

    # Check if the repository directory exists
    repo_path = os.path.join(custom_nodes_dir, repo_name)
    if not os.path.isdir(repo_path):
        print(f"Repository {repo_name} not found. Skipping.")
        continue

    # Get the latest commit on the main branch
    latest_commit = get_latest_commit(repo_path)

    if latest_commit is None:
        print(f"Failed to fetch latest commit for {repo_name}. Skipping.")
        continue

    if latest_commit[:7] != current_commit[:7]:
        print(f"Update available for {repo_name}")
        print(f"Current commit: {current_commit[:7]}")
        print(f"Latest commit: {latest_commit[:7]}")

        # Generate GitHub comparison URL
        compare_url = f"{repo_url}/compare/{current_commit[:7]}...{latest_commit[:7]}"
        print(f"Comparison URL: {compare_url}")

        response = input("Do you want to update? (y/n): ")
        if response.lower() == "y":
            print(f"Updating {repo_name}...")
            subprocess.run(
                ["git", "checkout", latest_commit], cwd=repo_path, check=True
            )
            subprocess.run(
                ["git", "submodule", "update", "--init", "--recursive"],
                cwd=repo_path,
                check=True,
            )

            repo["commit"] = latest_commit[:7]
            update_json_file(repos)
            update_changelog(repo_name, compare_url)

            print(f"Updated {repo_name} to {latest_commit[:7]}")
        else:
            print(f"Skipping update for {repo_name}")
    else:
        print(f"{repo_name} is up to date")

print(
    "\nFinished checking for updates. custom_nodes.json and CHANGELOG.md have been updated if necessary."
)
