import os

def get_size_in_mb(size_in_bytes):
    return size_in_bytes / (1024 * 1024)

def color_size(size_in_mb):
    if size_in_mb < 1:
        return 'green'
    elif size_in_mb < 10:
        return 'yellow'
    else:
        return 'red'

file_sizes = []
for root, dirs, files in os.walk('.'):
    for name in files:
        file_path = os.path.join(root, name)
        try:
            size = os.path.getsize(file_path)
            file_sizes.append((file_path, size))
        except OSError as e:
            print("Error with file:", file_path)
            print(e)
file_sizes.sort(key=lambda x: x[1], reverse=True)

for file_path, size in file_sizes:
    size_in_mb = get_size_in_mb(size)
    if size_in_mb >= 10:
        print(f"{file_path}: {size_in_mb:.2f} MB")
