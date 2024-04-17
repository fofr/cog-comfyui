#!/usr/bin/env python3

import json
import os
import sys

# Ensure the script can import WeightsManifest from the parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from weights_manifest import WeightsManifest

def main():
    # Load the JSON data from a file
    with open('weights.json', 'r') as file:
        data = json.load(file)

    # Sort each array in the JSON data
    for key in data:
        if isinstance(data[key], list):
            data[key].sort(key=str.casefold)

    # Write the sorted JSON data back to the file
    with open('weights.json', 'w') as file:
        json.dump(data, file, indent=2)

    WeightsManifest().write_supported_weights()

if __name__ == "__main__":
    main()
