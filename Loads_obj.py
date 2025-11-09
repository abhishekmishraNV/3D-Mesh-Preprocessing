import numpy as np
import os

# Folder containing all .obj files
folder_path = "8samples"

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".obj"):
        file_path = os.path.join(folder_path, file_name)
        vertices = []

        # Read the .obj file
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('v '):  # only vertex lines
                    parts = line.strip().split()
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])

        vertices = np.array(vertices)
        print(f"\nLoaded '{file_name}' with {vertices.shape[0]} vertices.")
        print(vertices[:5])  # show first 5 vertices of each mesh

