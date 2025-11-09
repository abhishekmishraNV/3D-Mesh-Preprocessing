import numpy as np
import os

# Path to normalized meshes folder
folder_path = "D:/Meshes/8samples"

# number of bins to quantize (e.g., 10-bit quantization)
n_bins = 1024  

for file_name in os.listdir(folder_path):
    if file_name.endswith(".obj"):
        file_path = os.path.join(folder_path, file_name)
        vertices = []

        # Load vertices from file
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])

        vertices = np.array(vertices)

        # --- Normalization (as before) ---
        v_min = vertices.min(axis=0)
        v_max = vertices.max(axis=0)
        normalized = (vertices - v_min) / (v_max - v_min)

        # --- Quantization ---
        quantized = np.floor(normalized * (n_bins - 1)).astype(int)

        # --- Dequantization ---
        dequantized = quantized / (n_bins - 1)

        # --- Denormalization (reversing normalization) ---
        reconstructed = dequantized * (v_max - v_min) + v_min

        # --- Error Analysis ---
        mse = np.mean((vertices - reconstructed) ** 2)
        mae = np.mean(np.abs(vertices - reconstructed))

        print(f"\nFile: {file_name}")
        print(f"MSE: {mse:.8f}, MAE: {mae:.8f}")
        print("First 3 quantized vertices:\n", quantized[:3])
        print("First 3 reconstructed vertices:\n", reconstructed[:3])
