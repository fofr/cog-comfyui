#!/bin/bash

# This script is used to clone specific versions of repositories.
# It takes a list of repositories and their commit hashes, clones them into a specific directory,
# and then checks out to the specified commit.

# List of repositories and their commit hashes to clone
# Each entry in the array is a string containing the repository URL and the commit hash separated by a space.
repos=(
  "https://github.com/cubiq/ComfyUI_IPAdapter_plus 0d0a7b3"
  "https://github.com/Fannovel16/comfyui_controlnet_aux 6d6f63c"
  "https://github.com/fofr/ComfyUI-Impact-Pack 07a18e7"
  "https://github.com/ltdrdata/ComfyUI-Inspire-Pack c8231dd"
  "https://github.com/theUpsider/ComfyUI-Logic fb88973"
  "https://github.com/Acly/comfyui-tooling-nodes bcb591c"
  "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved f9e0343"
  "https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite 5b5026c"
  "https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet fbf005f"
  "https://github.com/jags111/efficiency-nodes-comfyui 3b7e89d"
  "https://github.com/Derfuu/Derfuu_ComfyUI_ModdedNodes 2ace4c4"
  "https://github.com/FizzleDorf/ComfyUI_FizzNodes cd6cadd"
  "https://github.com/TinyTerra/ComfyUI_tinyterraNodes eda8a09"
  "https://github.com/ssitu/ComfyUI_UltimateSDUpscale bcefc5b"
  "https://github.com/cubiq/ComfyUI_essentials c9236fe"
  "https://github.com/shiimizu/ComfyUI-PhotoMaker-Plus 4c61084"
  "https://github.com/pythongosssss/ComfyUI-Custom-Scripts 9916c13"
  "https://github.com/BadCafeCode/masquerade-nodes-comfyui 240209b"
  "https://github.com/Gourieff/comfyui-reactor-node ae81f62"
  "https://github.com/cubiq/ComfyUI_InstantID 8b7932a"
  "https://github.com/WASasquatch/was-node-suite-comfyui 33534f2"
  "https://github.com/fofr/comfyui_segment_anything 8bc6178"
  "https://github.com/ZHO-ZHO-ZHO/ComfyUI-BRIA_AI-RMBG 44a3f8f"
  "https://github.com/Suzie1/ComfyUI_Comfyroll_CustomNodes d78b780"
  "https://github.com/huchenlei/ComfyUI-layerdiffuse 151f746"
  "https://github.com/kijai/ComfyUI-KJNodes 48d5a18"
  "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation 5e11679"
)

# Destination directory
# This is where the repositories will be cloned into.
dest_dir="ComfyUI/custom_nodes/"

# Loop over each repository in the list
for repo in "${repos[@]}"; do
  # Extract the repository URL and the commit hash from the string
  repo_url=$(echo $repo | cut -d' ' -f1)
  commit_hash=$(echo $repo | cut -d' ' -f2)

  # Extract the repository name from the URL by removing the .git extension
  repo_name=$(basename "$repo_url" .git)

  # Check if the repository directory already exists
  if [ ! -d "$dest_dir$repo_name" ]; then
    # Clone the repository into the destination directory
    echo "Cloning $repo_url into $dest_dir$repo_name and checking out to commit $commit_hash"
    git clone --recursive "$repo_url" "$dest_dir$repo_name"

    # Use a subshell to avoid changing the main shell's working directory
    # Inside the subshell, change to the repository's directory and checkout to the specific commit
    (
      cd "$dest_dir$repo_name" && git checkout "$commit_hash"
      rm -rf .git

      # Recursively remove .git directories from submodules
      find . -type d -name ".git" -exec rm -rf {} +

      # If the repository is efficiency-nodes-comfyui, also remove the images directory
      if [ "$repo_name" = "efficiency-nodes-comfyui" ]; then
        echo "Removing images and workflows directories from $repo_name"
        rm -rf images workflows
      fi
    )
  else
    echo "Skipping clone for $repo_name, directory already exists"
  fi
done

# Copy the was_suite_config.json to the appropriate directory
cp custom_node_configs/was_suite_config.json "$dest_dir"was-node-suite-comfyui/
