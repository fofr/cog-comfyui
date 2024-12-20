#!/usr/bin/env python3

import json
import os
import subprocess
import sys
from datetime import datetime
from urllib.parse import urlparse

"""
This script adds a new custom node repository to custom_nodes.json.
It clones the repository, gets the latest commit, and updates the JSON file and changelog.
"""

json_file = "custom_nodes.json"
comfy_dir = "ComfyUI"
custom_nodes_dir = f"{comfy_dir}/custom_nodes/"
changelog_file = "CHANGELOG.md"


def validate_github_url(url):
    """Validate and normalize GitHub URL."""
    try:
        parsed = urlparse(url)
        if parsed.netloc != "github.com":
            return None
        # Remove any trailing .git
        path = parsed.path.rstrip(".git")
        return f"https://github.com{path}"
    except Exception:
        return None


def get_repo_name(url):
    """Extract repository name from GitHub URL."""
    return os.path.basename(urlparse(url).path.rstrip(".git"))


def clone_repository(url, repo_name):
    """Clone the repository to custom_nodes directory."""
    repo_path = os.path.join(custom_nodes_dir, repo_name)
    if os.path.exists(repo_path):
        print(f"Error: Repository directory {repo_path} already exists!")
        sys.exit(1)

    try:
        subprocess.run(
            ["git", "clone", url, repo_path],
            check=True,
            capture_output=True,
            text=True,
        )
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=repo_path,
            check=True,
        )
        return repo_path
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        sys.exit(1)


def get_latest_commit(repo_path):
    """Get the latest commit hash from the repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting latest commit: {e}")
        sys.exit(1)


def update_json_file(url, commit):
    """Update custom_nodes.json with new repository."""
    try:
        if os.path.exists(json_file):
            with open(json_file, "r") as f:
                repos = json.load(f)
        else:
            repos = []

        # Check if repo already exists
        if any(repo["repo"] == url for repo in repos):
            print(f"Error: Repository {url} already exists in {json_file}")
            sys.exit(1)

        repos.append({"repo": url, "commit": commit[:7]})

        with open(json_file, "w") as f:
            json.dump(repos, f, indent=2)
            f.write("\n")

    except Exception as e:
        print(f"Error updating JSON file: {e}")
        sys.exit(1)


def update_changelog(repo_name, repo_url):
    """Update CHANGELOG.md with new repository."""
    today = datetime.now().strftime("%Y-%m-%d")
    update_line = f"- [Add {repo_name}]({repo_url}) custom node\n"

    try:
        if os.path.exists(changelog_file):
            with open(changelog_file, "r") as f:
                content = f.readlines()
        else:
            content = [f"# Changelog\n\n## {today}\n\n"]

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
            content.insert(today_index + 1, update_line)
        else:
            content.insert(2, update_line)

        with open(changelog_file, "w") as f:
            f.writelines(content)

    except Exception as e:
        print(f"Error updating changelog: {e}")
        sys.exit(1)


def log_requirements(repo_path):
    """Log the contents of requirements.txt if it exists."""
    req_file = os.path.join(repo_path, "requirements.txt")
    if os.path.exists(req_file):
        print("\nRequirements from requirements.txt:")
        try:
            with open(req_file, "r") as f:
                print(f.read())
        except Exception as e:
            print(f"Error reading requirements.txt: {e}")
    else:
        print("\nNo requirements.txt found in repository")


def main():
    if len(sys.argv) != 2:
        print("Usage: python add_custom_node.py <github_url>")
        sys.exit(1)

    github_url = validate_github_url(sys.argv[1])
    if not github_url:
        print("Error: Invalid GitHub URL")
        sys.exit(1)

    repo_name = get_repo_name(github_url)
    print(f"\nAdding custom node: {repo_name}")

    # Clone repository
    repo_path = clone_repository(github_url, repo_name)
    print(f"Cloned repository to {repo_path}")

    # Get latest commit
    commit = get_latest_commit(repo_path)
    print(f"Latest commit: {commit[:7]}")

    # Update JSON file
    update_json_file(github_url, commit)
    print(f"Updated {json_file}")

    # Update changelog
    update_changelog(repo_name, github_url)
    print(f"Updated {changelog_file}")

    # Log requirements
    log_requirements(repo_path)

    print("\nCustom node added successfully!")


if __name__ == "__main__":
    main()
