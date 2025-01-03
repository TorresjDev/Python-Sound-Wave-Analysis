# 🎶 **Sound Wave Analysis Project** 🌊

This project brings **sound waves** to life through **visualizations** and **decibel analysis** using Python! Perfect for exploring the **physics of sound** and understanding amplitude, frequency, and dB levels. Dive into the world of audio signals with **interactive graphs** and insightful data. 🌟

---

## 🛠️ **Project Features**

- 🎧 **Waveform Visualization**: See the amplitude of your audio over time.
- 📈 **Frequency Spectrum**: Explore the spectrogram and uncover hidden frequencies.
- 🔊 **Decibel Analysis**:
  - Calculate **peak** and **minimum dB** values.
  - Compare relative levels with **dBFS** (Decibels Full Scale).
  - Understand sound intensity using **RMS dB**.

---

## 🚀 **How to Use**

### 1️⃣ **Setup**

1. **Install Python** and required libraries:
   ```bash
   pip install numpy matplotlib
   ```
2. Replace the sample `.wav` file with your own in the `sounds/` folder.

---

### 2️⃣ **Run the Code**

- **Terminal**:
  ```bash
  python sound_analysis.py
  ```
- **Jupyter Notebook**:
  - Install Jupyter if not already:
    ```bash
    pip install notebook
    ```
  - Open the notebook:
    ```bash
    jupyter notebook sound-wave-analysis.ipynb
    ```
  - Run the cells for **step-by-step visualization**.

---

### 3️⃣ **Switch Audio Files**

🎵 Want to analyze new sounds? Replace `"sounds/decibel-10s.wav"` in the code with your `.wav` file. Make sure it’s in the same folder!

---

## 📖 **Key Concepts**

- **Waveform**: Shows amplitude vs. time.
- **Amplitude**: The height of the wave, representing loudness.
- **Frequency**: Measured in Hz, determines the pitch.
- **dBFS**: Relative sound levels in decibels.
- **Spectrogram**: Visualizes frequency over time.

---

## 📂 **Folder Structure**

```
/project-folder
│
├── sounds/                  # 🎵 Audio files
├── sound_analysis.py        # 📊 Main script
├── sound_tools.py           # 🛠️ Helper functions
├── sound_visualization.py   # 🎨 Plotting tools
├── sound-wave-analysis.ipynb # 💻 Jupyter Notebook
└── README.md                # 📜 Documentation
```

---

## 🌟 **How It Works**

1. The program **reads a `.wav` file** to extract amplitude and frequency data.
2. **Decibel calculations** provide insights into sound intensity.
3. **Visualizations** are created:
   - **Waveform**: Shows how amplitude changes over time.
   - **Spectrogram**: Displays the frequency spectrum with intensity.

---

## 🖥️ **Tips**

- 💡 Adjust the spectrogram settings (`vmin`, `vmax`, etc.) for clearer visuals.
- 🎨 Use different `.wav` files to explore varying sound characteristics!

---

## 📚 **References**

- Python Libraries: `Wave`, `NumPy`, `Matplotlib`
- Sound Physics Resources: [Wikipedia - Sound](https://en.wikipedia.org/wiki/Sound)

**Happy Coding & Visualizing!** ✨
