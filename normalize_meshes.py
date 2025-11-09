import numpy as np
import os

folder_path = "8samples"

for file_name in os.listdir(folder_path):
    if file_name.endswith(".obj"):
        path = os.path.join(folder_path, file_name)
        verts = []

        # reading vertices
        with open(path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.strip().split()
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    verts.append([x, y, z])

        verts = np.array(verts)

        # normalization
        min_val = verts.min(axis=0)
        max_val = verts.max(axis=0)
        norm_verts = (verts - min_val) / (max_val - min_val)

        print(f"\nFile: {file_name}")
        print("Min:", min_val)
        print("Max:", max_val)
        print("First 5 normalized vertices:")
        print(norm_verts[:5])

