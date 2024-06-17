import json
from collections import defaultdict

# Read JSON data from 'duplicate.json'
with open('dublicate.json', 'r') as f:
    data = json.load(f)

# Use defaultdict to combine values for duplicate keys within the "responses" dictionary
merged_data = defaultdict(list)

# Iterate through the "responses" dictionary
for key, value in data["responses"].items():
    merged_data[key].extend(value)

# Convert defaultdict back to a regular dictionary
merged_responses = dict(merged_data)

# Create the final structure with the merged responses
final_data = {"responses": merged_responses}

# Save merged data to 'conversation.json'
with open('conversation.json', 'w') as f:
    json.dump(final_data, f, indent=2)

print("Merged data has been saved to 'conversation.json'")
