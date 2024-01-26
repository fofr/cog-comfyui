import json

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
