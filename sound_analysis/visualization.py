"""
Sound Analysis Visualization

Plotting and visualization functions for audio analysis.
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_waveform(waveform, sample_rate, duration, title="Audio Waveform", save_path=None):
    """Plot the audio waveform."""
    time = np.linspace(0, duration, num=len(waveform))
    
    plt.figure(figsize=(12, 6))
    plt.plot(time, waveform, color='blue', linewidth=0.5)
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel('Amplitude', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📁 Waveform saved to: {save_path}")
    
    plt.show()


def plot_spectrogram(waveform, sample_rate, title="Frequency Spectrogram", save_path=None):
    """Plot the frequency spectrogram."""
    plt.figure(figsize=(12, 6))
    plt.specgram(waveform, Fs=sample_rate, vmin=-20, vmax=50, cmap='viridis')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel('Frequency (Hz)', fontsize=12)
    plt.colorbar(label="Intensity (dB)")
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"📁 Spectrogram saved to: {save_path}")
    
    plt.show()


def plot_frequency_analysis(waveform, sample_rate, title="Frequency Analysis"):
    """Plot frequency domain analysis."""
    # Compute FFT
    fft = np.fft.fft(waveform)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    magnitude = np.abs(fft)
    
    # Only plot positive frequencies
    positive_freqs = freqs[:len(freqs)//2]
    positive_magnitude = magnitude[:len(magnitude)//2]
    
    plt.figure(figsize=(12, 6))
    plt.plot(positive_freqs, 20 * np.log10(positive_magnitude + 1e-10))
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Frequency (Hz)', fontsize=12)
    plt.ylabel('Magnitude (dB)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_combined_analysis(waveform, sample_rate, duration, filename):
    """Create a combined visualization with multiple plots."""
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f"Complete Analysis: {filename}", fontsize=16, fontweight='bold')
    
    # Time domain plot
    time = np.linspace(0, duration, num=len(waveform))
    axes[0, 0].plot(time, waveform, color='blue', linewidth=0.5)
    axes[0, 0].set_title('Waveform')
    axes[0, 0].set_xlabel('Time (seconds)')
    axes[0, 0].set_ylabel('Amplitude')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Frequency domain plot
    fft = np.fft.fft(waveform)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    magnitude = np.abs(fft)
    positive_freqs = freqs[:len(freqs)//2]
    positive_magnitude = magnitude[:len(magnitude)//2]
    
    axes[0, 1].plot(positive_freqs, 20 * np.log10(positive_magnitude + 1e-10))
    axes[0, 1].set_title('Frequency Spectrum')
    axes[0, 1].set_xlabel('Frequency (Hz)')
    axes[0, 1].set_ylabel('Magnitude (dB)')
    axes[0, 1].grid(True, alpha=0.3)
    
    # Spectrogram
    axes[1, 0].specgram(waveform, Fs=sample_rate, vmin=-20, vmax=50, cmap='viridis')
    axes[1, 0].set_title('Spectrogram')
    axes[1, 0].set_xlabel('Time (seconds)')
    axes[1, 0].set_ylabel('Frequency (Hz)')
    
    # Amplitude histogram
    axes[1, 1].hist(waveform, bins=50, alpha=0.7, color='green')
    axes[1, 1].set_title('Amplitude Distribution')
    axes[1, 1].set_xlabel('Amplitude')
    axes[1, 1].set_ylabel('Count')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
