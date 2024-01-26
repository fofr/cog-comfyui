import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from weights_downloader import WeightsDownloader

def main(filename):
    wd = WeightsDownloader()
    wd.download_weights(filename)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_weights.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    main(filename)
