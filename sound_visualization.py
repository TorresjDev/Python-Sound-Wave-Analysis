import numpy as np # Python library for numerical operations
import matplotlib.pyplot as plt # Python library for plotting data

def plot_signal(waveform, sample_rate, duration, channel):
      """
      Plots the audio signal waveform.
   
      Args:
         waveform (np.array): The audio signal waveform.
         sample_rate (int): The sample rate of the audio signal.
         duration (float): The duration of the audio signal in seconds.
      """
      time = np.linspace(0, duration, num=len(waveform))
      plt.figure(figsize=(10, 4))
      plt.plot(time, waveform, label=f'{channel} Signal', color='blue')
      plt.title(f'{channel} Signal Waveform')
      plt.xlabel('Time [s]')
      plt.ylabel('Amplitude')
      plt.xlim(0, duration)
      # plt.ylim(0, sample_rate * 2)
      plt.grid(True)
      plt.show()


def plot_spectrogram(waveform, sample_rate):
      """
      Plots the spectrogram of the audio signal.
   
      Args:
         waveform (np.array): The audio signal waveform.
         sample_rate (int): The sample rate of the audio signal.
      """
      plt.figure(figsize=(15, 5))
      plt.specgram(waveform, Fs=sample_rate, vmin=-20, vmax=50)
      plt.title(f'Frequency Spectrogram')
      plt.xlabel('Time [s]')
      plt.ylabel('Frequency [Hz]')
      plt.ylim(0, sample_rate / 2)
      plt.xlim(0, len(waveform) / sample_rate)
      plt.colorbar(label="Intensity (dB)")
      plt.show()