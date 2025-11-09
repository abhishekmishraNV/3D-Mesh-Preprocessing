===========================================
3D Mesh Normalization, Quantization, and Analysis
===========================================


-------------------------------------------
Project Overview
-------------------------------------------
This project explores practical steps to get 3D mesh data ready for machine learning and AI applications. 
The process mostly covers:

• Normalization: Adjusting all mesh vertex coordinates so they're within a similar range for consistency.

• Quantization: Lowering the level of detail in the data on purpose, mainly to save space.

• Reconstruction: Trying to bring the quantized mesh back to a version as close as possible to the original.

• Error Checking: Measuring how accurate our reconstruction is, using common metrics like 
  Mean Squared Error (MSE) and Mean Absolute Error (MAE).

The pipeline here is a simplified test-bed, inspired by approaches in recent 3D AI research, 
like SeamGPT, but made easy to follow for practical coursework.

-------------------------------------------
What’s in Each File?
-------------------------------------------

File/Folder           | What it Does
-------------------------------------------------------------
mesh_pipeline.py       | Loads mesh files and runs the full normalization, quantization, and reconstruction chain. 
                        Results are printed and saved.

Mesh_Analysis.ipynb    | Jupyter notebook for walking through the process interactively, with code explanations, 
                        charts, and widgets to tweak settings.

8samples/              | Folder with the .obj mesh files for testing.

outputs/               | Where saved meshes and result plots end up.

-------------------------------------------
How to Run the Code
-------------------------------------------

Option 1: Automated Script
--------------------------
1. Open VS Code and start a terminal.
2. Run:
   python mesh_pipeline.py
3. The script will handle all meshes found in 8samples/.
4. Find processed outputs (meshes, plots, reports) in the outputs/ directory.

Option 2: Interactive Notebook
-------------------------------
1. Open Mesh_Analysis.ipynb in VS Code or Jupyter Notebook.
2. Execute sections one at a time by clicking or pressing Shift + Enter.
3. Watch plots and results appear step-by-step.
4. Try using the interactive quantization slider — see error changes in real time.

-------------------------------------------
Results
-------------------------------------------
• Each mesh is evaluated for reconstruction accuracy, including MSE and MAE.
• Quantized and reconstructed vertex data are available for spot checks.
• Matplotlib graphs help visualize how errors change across different meshes.

-------------------------------------------
What You’ll Learn
-------------------------------------------
✓ How to process and prepare 3D mesh data for AI work.
✓ How normalization, quantization, and error analysis are implemented.
✓ The trade-offs in mesh quality due to preprocessing.
✓ Building both automated and interactive data workflows.
