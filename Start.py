import os

# Define the folder and file structure
structure = {
    "Friday": [
        "Brain/data/application_map.json",
    ]
}

# Create directories and files based on the structure
for root, files in structure.items():
    for file_path in files:
        # Create full file path
        full_path = os.path.join(root, file_path)
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        # Create the file
        open(full_path, 'a').close()

print("Folder structure created successfully.")
