# 🌊 Sound Wave Analysis

A professional, web-based tool for analyzing and visualizing audio files. Built with **Streamlit** and **Plotly**, this application provides physics-grade analysis of sound waves, supporting WAV, MP3, and FLAC formats.

![App Screenshot](https://raw.githubusercontent.com/TorresjDev/Python-Sound-Wave-Analysis/main/assets/app_preview.png)
*(Note: Replace with actual screenshot path once pushed)*

## 🚀 Features

### 📊 Professional Visualization
- **Waveform**: Interactive time-domain display.
- **Frequency Spectrum**: Audacity-style spectrum analysis with log scale frequency and dB.
- **Spectrogram**: Time-frequency intensity heatmap.
- **Power Spectral Density (PSD)**: Energy distribution across frequencies.
- **Phase Response**: Phase angle vs. frequency.
- **Amplitude Histogram**: Distribution of signal amplitudes.

### 🔬 Detailed Analysis
- **Audio Metrics**: Sample rate, duration, channels, RMS dB, dynamic range.
- **Harmonic Detection**: Identifies fundamental frequency and up to 5 overtones.
- **Speed of Sound Calculator**: Real-time calculator for various media (Air, Water, Steel, etc.) with temperature adjustment.

### 🛠️ Key Capabilities
- **Multi-Format Support**: Upload WAV, MP3, or FLAC files (auto-converted).
- **Audio Playback**: Listen to your audio directly in the browser.
- **Interactive UI**: Native Dark/Light mode support (toggles via Streamlit Settings).
- **Export Options**: Download analysis data as CSV or a text summary.

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Visualization**: [Plotly](https://plotly.com/python/)
- **Audio Processing**: [NumPy](https://numpy.org/), [SciPy](https://scipy.org/), [Pydub](https://github.com/jiaaro/pydub)
- **Deployment**: Streamlit Cloud

## 📦 Installation & Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/TorresjDev/Python-Sound-Wave-Analysis.git
   cd Python-Sound-Wave-Analysis
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: For MP3/FLAC support, ensure you have [ffmpeg](https://ffmpeg.org/) installed on your system.*

3. **Run the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open in browser:**
   The app will automatically open at `http://localhost:8501`.

## ☁️ Deployment

### Deploying to Streamlit Cloud

1. Push your code to GitHub.
2. Sign in to [Streamlit Cloud](https://share.streamlit.io/).
3. Click **"New App"**.
4. Select your repository (`TorresjDev/Python-Sound-Wave-Analysis`), branch (`main`), and main file (`streamlit_app.py`).
5. Click **"Deploy"**.

Streamlit Cloud will automatically detect `packages.txt` (if added for ffmpeg) and `requirements.txt` to install dependencies.

## 🧪 CI/CD

This project uses **GitHub Actions** for continuous integration:
- **Python Linting**: Checks for syntax errors and coding standards.
- **Dependency Test**: Verifies that `requirements.txt` installs correctly.
- **Streamlit Config Check**: Ensures the app configuration is valid.

## 📜 License

This project is licensed under the CC BY-NC 4.0 License.

---
**Created by [TorresjDev](https://github.com/TorresjDev)**
