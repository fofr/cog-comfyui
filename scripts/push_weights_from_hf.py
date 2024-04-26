#!/usr/bin/env python
import urllib.request
from html.parser import HTMLParser
import argparse
import os

# URL to be scraped
default_url = "https://huggingface.co/guoyww/animatediff/tree/cd71ae134a27ec6008b968d6419952b0c0494cf2"


# HTML Parser to extract all '?download' links
class DownloadLinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.download_urls = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr in attrs:
                if attr[0] == "href" and "?download" in attr[1]:
                    print(attr[1])
                    file_extension = os.path.splitext(attr[1].split("?")[0])[1]
                    if file_extension in [
                        ".ckpt",
                        ".safetensors",
                        ".pt",
                        ".pth",
                        ".bin",
                        ".onnx",
                        ".torchscript",
                    ]:
                        filename = os.path.basename(attr[1].split("?")[0])
                        self.download_urls.append(
                            ("https://huggingface.co" + attr[1], filename)
                        )


# Function to scrape the URL and extract all '?download' links
def extract_download_links(url):
    try:
        # Sending a request to the URL
        response = urllib.request.urlopen(url)
        # If the request was successful
        if response.status == 200:
            # Using HTMLParser to parse the HTML content
            parser = DownloadLinkExtractor()
            parser.feed(response.read().decode())
            return parser.download_urls
        else:
            return f"Failed to access the URL. Status code: {response.status}"
    except Exception as e:
        return f"An error occurred: {e}"


# Function to save the download links to a file
def save_to_file(download_urls):
    with open("weights.txt", "w") as f:
        for url, filename in download_urls:
            print(f"{url} {filename}")
            f.write("%s %s\n" % (url, filename))


# Parsing command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("url", nargs='?', default=default_url, type=str, help="URL to be scraped")
args = parser.parse_args()

# Extracting the download links
download_urls = extract_download_links(args.url)

# Saving the download links to a file
save_to_file(download_urls)
