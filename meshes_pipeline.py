"""
Mesh Quantization & Reconstruction Pipeline
-------------------------------------------
This script loads all .obj meshes from a given folder,
normalizes vertices (two methods), quantizes them, reconstructs,
and analyses reconstruction error (MSE, MAE, per-axis plots).

Author: AI-Generated (Custom for Abhishek, 2025)
"""

import numpy as np
import os
import matplotlib.pyplot as plt
import csv

# ---------------------- CONFIGURATION ----------------------

FOLDER_PATH = "8samples"      # Folder containing your .obj files
N_BINS = 1024                 # Quantization bins (e.g., 10-bit = 1024)
SAVE_RESULTS = True           # Whether to save normalized & reconstructed meshes
SUMMARY_FILE = "mesh_summary.csv"

# ---------------------- HELPER FUNCTIONS ----------------------

def load_obj_vertices(file_path):
    """Load vertices from a Wavefront .obj file."""
    verts = []
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):  # only vertex lines
                parts = line.strip().split()
                verts.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return np.array(verts)


def save_obj(file_path, verts):
    """Save vertices back to a .obj file (no faces)."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        for v in verts:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")


def normalize_minmax(verts):
    """Min–Max normalization to [0, 1] per axis."""
    v_min = verts.min(axis=0)
    v_max = verts.max(axis=0)
    normalized = (verts - v_min) / (v_max - v_min)
    return normalized, v_min, v_max


def normalize_unit_sphere(verts):
    """Center and scale vertices so they fit inside a unit sphere."""
    centered = verts - verts.mean(axis=0)
    radius = np.linalg.norm(centered, axis=1).max()
    normalized = centered / radius
    return normalized, verts.mean(axis=0), radius


def quantize(verts, n_bins):
    """Quantize normalized vertices into discrete bins."""
    return np.floor(verts * (n_bins - 1)).astype(int)


def dequantize(quantized, n_bins):
    """Dequantize back to floating-point normalized coordinates."""
    return quantized / (n_bins - 1)


def compute_errors(original, reconstructed):
    """Compute MSE, MAE and per-axis errors."""
    mse = np.mean((original - reconstructed) ** 2)
    mae = np.mean(np.abs(original - reconstructed))
    per_axis = np.mean((original - reconstructed) ** 2, axis=0)
    return mse, mae, per_axis


def plot_per_axis_error(per_axis, file_name):
    """Plot per-axis reconstruction error."""
    axes = ['X', 'Y', 'Z']
    plt.bar(axes, per_axis)
    plt.title(f"Per-Axis Reconstruction Error: {file_name}")
    plt.ylabel("Mean Squared Error")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()


# ---------------------- MAIN PIPELINE ----------------------

def main():
    results = []  # for CSV summary

    for fname in os.listdir(FOLDER_PATH):
        if not fname.endswith(".obj"):
            continue

        path = os.path.join(FOLDER_PATH, fname)
        verts = load_obj_vertices(path)

        # --- Mesh statistics (Task 1) ---
        print(f"\n📂 File: {fname}")
        print(f"  Number of vertices: {len(verts)}")
        print(f"  Min per axis: {verts.min(axis=0)}")
        print(f"  Max per axis: {verts.max(axis=0)}")
        print(f"  Mean per axis: {verts.mean(axis=0)}")
        print(f"  Std per axis: {verts.std(axis=0)}")

        # --- Choose normalization method (you can loop both) ---
        for method in ["minmax", "unitsphere"]:
            if method == "minmax":
                normalized, p1, p2 = normalize_minmax(verts)
            else:
                normalized, p1, p2 = normalize_unit_sphere(verts)

            # --- Quantization ---
            quantized = quantize(normalized, N_BINS)
            dequantized = dequantize(quantized, N_BINS)

            # --- Denormalization / Reconstruction ---
            if method == "minmax":
                reconstructed = dequantized * (p2 - p1) + p1
            else:
                reconstructed = dequantized * p2 + p1

            # --- Error analysis ---
            mse, mae, per_axis = compute_errors(verts, reconstructed)

            print(f"  [{method.upper()}] MSE: {mse:.8f}, MAE: {mae:.8f}")
            print(f"  First 3 quantized vertices:\n{quantized[:3]}")
            print(f"  First 3 reconstructed vertices:\n{reconstructed[:3]}")

            # --- Save results ---
            if SAVE_RESULTS:
                out_norm = os.path.join("output_normalized", method, fname)
                out_recon = os.path.join("output_reconstructed", method, fname)
                save_obj(out_norm, normalized)
                save_obj(out_recon, reconstructed)

            # --- Plot per-axis error ---
            plot_per_axis_error(per_axis, f"{fname} ({method})")

            # --- Collect for summary ---
            results.append([fname, method, mse, mae] + list(per_axis))

    # --- Write summary CSV ---
    if SAVE_RESULTS and results:
        with open(SUMMARY_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["File", "Method", "MSE", "MAE", "MSE_X", "MSE_Y", "MSE_Z"])
            writer.writerows(results)
        print(f"\n✅ Summary saved to {SUMMARY_FILE}")


# ---------------------- ENTRY POINT ----------------------

if __name__ == "__main__":
    main()
