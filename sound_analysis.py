import wave # Python library for reading and writing sound files
import matplotlib.pyplot as plt # Python library for plotting data
from sound_tools import wave_info, wave_to_db, wave_to_db_rms, wave_to_dbfs,detect_db_range
from sound_visualization import plot_signal, plot_spectrogram

# Load and read the WAV file
wav_obj = wave.open("sounds/decibel-10s.wav", "rb") # rb mode returns a "read only" object

sample_freq, total_samples, signal_duration, num_audio_channel, raw_signal_wave, signal_amplitude_array = wave_info(wav_obj)

print(f"Sample frequency: {sample_freq} Hz")
print(f"Number of samples: {total_samples}")
print(f"Duration of the sound file: {signal_duration} s")
print(f"Number of audio channels: {num_audio_channel}")
# print(f"Audio data: {raw_signal_wave}")
print(f"Audio data as numpy array: {signal_amplitude_array}")

# Check for mono or stereo and handle accordingly
channel_type = "audio"
waveform = None
if num_audio_channel == 1:  # Mono audio
    print("Mono audio detected.")
    l_channel = signal_amplitude_array  # sound channel
    r_channel = None  # No right channel for mono
    channel_type = "Mono Audio"
    waveform = l_channel
else:  # Stereo audio
    print("Stereo audio detected.")
    l_channel = signal_amplitude_array[0::2]  # Left channel
    r_channel = signal_amplitude_array[1::2]  # Right channel
    channel_type = "Stereo Audio"
    waveform = l_channel

#  Calculate the waveform in decibels (dB)
waveform_db = wave_to_db(waveform)
print(f"Waveform in decibels: {waveform_db}")

# Calculate the waveform in decibels using the RMS value
waveform_db_rms = wave_to_db_rms(waveform)
print(f"Waveform in decibels using RMS value: {waveform_db_rms}")

# Find the highest and smallest dB levels
highest_dB, smallest_dB = detect_db_range(waveform)
print(f"Highest dB level: {highest_dB}")
print(f"Smallest dB level: {smallest_dB}")

# Calculate the waveform in decibels relative to full scale (dBFS)
waveform_dbfs = wave_to_dbfs(waveform)
print(f"Waveform in decibels relative to full scale: {waveform_dbfs}")

plot_signal(waveform, sample_freq, signal_duration, channel_type) # Plot the signal waveform

plot_spectrogram(waveform, sample_freq) # Plot the spectrogram