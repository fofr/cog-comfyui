import csv
import requests
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from weights_manifest import WeightsManifest

# Define the URL where the model list is located
MODEL_LIST_URL = "https://raw.githubusercontent.com/ltdrdata/ComfyUI-Manager/main/model-list.json"

# Function to download and parse the JSON file
def download_model_list(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
    return response.json()

# Function to load the already downloaded weights
def load_downloaded_weights():
    weights_map = WeightsManifest().weights_map
    downloaded_weights = set()
    for weight in weights_map.keys():
        downloaded_weights.add(weight)
    print(downloaded_weights)
    return downloaded_weights

# Function to write the list of URLs for not downloaded weights by type
def write_urls_by_type(data, not_downloaded_filename, downloaded_weights):
    urls_by_type = {}
    for model in data['models']:
        if model['type'] not in urls_by_type:
            urls_by_type[model['type']] = []
        if model['filename'] not in downloaded_weights:
            urls_by_type[model['type']].append((model['url'], model['filename']))

    for model_type, urls in urls_by_type.items():
        with open(f"{not_downloaded_filename}_{model_type}.txt", 'w') as file:
            for url, filename in urls:
                file.write(f"{url} {filename}\n")

# Main function to orchestrate the download and list creation
def main():
    try:
        # Load the already downloaded weights
        downloaded_weights = load_downloaded_weights()
        # Download the model list
        model_list = download_model_list(MODEL_LIST_URL)
        # Write the list of URLs for not downloaded weights by type
        write_urls_by_type(model_list, 'missing', downloaded_weights)
        print("URL lists created successfully.")
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

if __name__ == "__main__":
    main()
