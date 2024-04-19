#!/usr/bin/env python3
import sys
import os
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from weights_downloader import WeightsDownloader

def download_weight_files(weight_files):
    wd = WeightsDownloader()
    for weight_file in weight_files:
        wd.download_weights(weight_file)

def extract_weights_from_workflow(workflow_path):
    with open(workflow_path, 'r') as f:
        workflow = json.load(f)
    weights_to_download = []
    for node in workflow.values():
        if "inputs" in node:
            for input in node["inputs"].values():
                if isinstance(input, str) and input.endswith(tuple(WeightsDownloader.supported_filetypes)):
                    weights_to_download.append(input)
    return list(set(weights_to_download))

def main(filenames):
    weight_files = []
    for filename in filenames:
        if filename.endswith('.txt'):
            with open(filename, 'r') as f:
                weight_files.extend(f.read().splitlines())
        elif filename.endswith('.json'):
            weight_files.extend(extract_weights_from_workflow(filename))
        else:
            weight_files.append(filename)
    download_weight_files(weight_files)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_weights.py <filename> [<filename> ...] or python get_weights.py <weights.txt> or python get_weights.py <workflow.json>")
        sys.exit(1)
    filenames = sys.argv[1:]
    main(filenames)
