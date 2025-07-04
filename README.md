# SFD_BMD-Visualizer
# 🏗️ SFD & BMD Visualizer

This is a Python tool for visualizing **Shear Force Diagrams (SFD)** and **Bending Moment Diagrams (BMD)** for simply supported beams under various loading conditions.

It allows you to:
- Add **point loads** and **uniformly distributed loads (UDLs)**
- Automatically compute **support reactions**
- Plot and save **SFD and BMD diagrams**
- Organize your outputs with beam-specific filenames

---

## 📸 Example Output

<p align="center">
  <img src="Beam A.png" alt="Example Plot" width="700">
</p>

---

## 🧰 Features

- ✅ Add point loads at specific positions
- ✅ Add UDLs across any span of the beam
- ✅ Calculates reaction forces at supports
- ✅ Plots clean, professional SFD & BMD using Matplotlib
- ✅ Automatically saves the diagrams to a folder named `beam_outputs/`
- ✅ Custom file naming using the beam’s name

---

## 📦 Requirements

Python 3.6 or higher

Install required libraries with:
```bash
pip install -r requirements.txt
```

🚀 Usage
1.Clone or download this repository

2.Open sfd_bmd_visualizer.py in your IDE (e.g., VS Code)

3.Scroll to the bottom and define your beam:

  beam = Beam(length=10, name="beam_1_example")
  
  beam.add_point_load(pos=4, magnitude=-10)
  
  beam.add_udl(start=6, end=10, intensity=-2)   

4.Run the script:
  python sfd_bmd_visualizer.py
  
5.You'll see the plot and find the image saved at:
  beam_outputs/beam_1_example.png

