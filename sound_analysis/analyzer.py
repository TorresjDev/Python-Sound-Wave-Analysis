"""
Sound Analysis Analyzer

Core analysis functions for processing WAV files.
"""

import os
import wave
import numpy as np
from .tools import wave_to_db, wave_to_db_rms, detect_db_range, list_wav_files
from .visualization import plot_waveform, plot_spectrogram, plot_combined_analysis


def get_wave_info(file_path):
    """Get basic information about a WAV file."""
    try:
        wav_obj = wave.open(file_path, "rb")

        info = {
            'sample_rate': wav_obj.getframerate(),
            'total_samples': wav_obj.getnframes(),
            'channels': wav_obj.getnchannels(),
            'sample_width': wav_obj.getsampwidth(),
        }

        info['duration'] = info['total_samples'] / info['sample_rate']
        info['channel_type'] = "Mono" if info['channels'] == 1 else "Stereo"

        wav_obj.close()
        return info

    except Exception as e:
        raise Exception(f"Error reading WAV file info: {str(e)}")


def load_wave_data(file_path):
    """Load waveform data from a WAV file."""
    try:
        wav_obj = wave.open(file_path, "rb")

        # Get file info
        sample_rate = wav_obj.getframerate()
        total_samples = wav_obj.getnframes()
        channels = wav_obj.getnchannels()

        # Read audio data
        raw_data = wav_obj.readframes(total_samples)
        audio_data = np.frombuffer(raw_data, dtype=np.int16)

        # Handle mono/stereo
        if channels == 1:
            waveform = audio_data
        else:
            waveform = audio_data[0::2]  # Use left channel for stereo

        wav_obj.close()

        return {
            'waveform': waveform,
            'sample_rate': sample_rate,
            'duration': total_samples / sample_rate,
            'channels': channels
        }

    except Exception as e:
        raise Exception(f"Error loading WAV data: {str(e)}")


def analyze_audio_levels(waveform):
    """Analyze various audio level metrics."""
    # Basic statistics
    max_amplitude = np.max(np.abs(waveform))
    min_amplitude = np.min(np.abs(waveform))
    mean_amplitude = np.mean(np.abs(waveform))

    # Decibel calculations
    avg_db = wave_to_db(waveform)
    rms_db = wave_to_db_rms(waveform)
    db_range = detect_db_range(waveform)

    return {
        'max_amplitude': max_amplitude,
        'min_amplitude': min_amplitude,
        'mean_amplitude': mean_amplitude,
        'avg_db': avg_db,
        'rms_db': rms_db,
        'db_range': db_range
    }


def perform_complete_analysis(file_path, show_plots=True, save_figures=False):
    """Perform complete analysis of a WAV file."""
    try:
        # Get file info
        file_info = get_wave_info(file_path)

        # Load waveform data
        wave_data = load_wave_data(file_path)
        waveform = wave_data['waveform']
        sample_rate = wave_data['sample_rate']
        duration = wave_data['duration']

        # Analyze audio levels
        audio_levels = analyze_audio_levels(waveform)

        # Create filename for plots
        filename = os.path.basename(file_path)

        # Display results
        print("\n🎵 Analysis Results")
        print("=" * 40)
        print(f"📁 File: {filename}")
        print(f"📊 Sample Rate: {file_info['sample_rate']:,} Hz")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(
            f"🎧 Channels: {file_info['channels']} ({file_info['channel_type']})")
        print(f"📈 Total Samples: {file_info['total_samples']:,}")

        print(f"\n📈 Sound Levels:")
        print(f"🔊 Average dB: {audio_levels['avg_db']:.2f}")
        print(f"📊 RMS dB: {audio_levels['rms_db']:.2f}")
        print(
            f"📏 Dynamic Range: {audio_levels['db_range']['dynamic_range']:.2f} dB")
        print(f"📈 Max dB: {audio_levels['db_range']['max_db']:.2f}")
        print(f"📉 Min dB: {audio_levels['db_range']['min_db']:.2f}")

        # Generate visualizations
        if show_plots:
            print("\n🎨 Generating visualizations...")

            if save_figures:
                figures_dir = "figures"
                os.makedirs(figures_dir, exist_ok=True)
                base_name = os.path.splitext(filename)[0]

                waveform_path = os.path.join(
                    figures_dir, f"{base_name}_waveform.png")
                spectrogram_path = os.path.join(
                    figures_dir, f"{base_name}_spectrogram.png")
            else:
                waveform_path = None
                spectrogram_path = None

            plot_waveform(waveform, sample_rate, duration,
                          f"{filename} - Waveform", waveform_path)
            plot_spectrogram(waveform, sample_rate,
                             f"{filename} - Spectrogram", spectrogram_path)

            # Optional: Combined analysis plot
            # plot_combined_analysis(waveform, sample_rate, duration, filename)

        print("\n✅ Analysis completed!")

        return {
            'file_info': file_info,
            'wave_data': wave_data,
            'audio_levels': audio_levels
        }

    except Exception as e:
        print(f"❌ Error analyzing file: {str(e)}")
        return None
