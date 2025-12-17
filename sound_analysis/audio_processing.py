"""
Audio Processing Module

Handles audio format conversion, filtering, and advanced processing.
Supports WAV, MP3, and FLAC formats.
"""

import io
import tempfile
import os
import numpy as np
from scipy import signal
from scipy.io import wavfile

# Try to import pydub for MP3/FLAC support
try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False


def convert_audio_to_wav(uploaded_file, file_extension):
    """
    Convert uploaded audio file to WAV format.
    
    Supports: WAV, MP3, FLAC
    Returns: Path to temporary WAV file
    """
    if not PYDUB_AVAILABLE and file_extension != '.wav':
        raise ImportError("pydub is required for MP3/FLAC support. Install with: pip install pydub")
    
    # Create temp file for the uploaded content
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_input:
        tmp_input.write(uploaded_file.getvalue())
        tmp_input_path = tmp_input.name
    
    try:
        if file_extension == '.wav':
            # Already WAV, just return the path
            return tmp_input_path
        
        # Convert to WAV using pydub
        if file_extension == '.mp3':
            audio = AudioSegment.from_mp3(tmp_input_path)
        elif file_extension == '.flac':
            audio = AudioSegment.from_file(tmp_input_path, format='flac')
        else:
            audio = AudioSegment.from_file(tmp_input_path)
        
        # Export as WAV
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_output:
            tmp_output_path = tmp_output.name
        
        audio.export(tmp_output_path, format='wav')
        
        # Clean up input temp file
        os.unlink(tmp_input_path)
        
        return tmp_output_path
        
    except Exception as e:
        # Clean up on error
        if os.path.exists(tmp_input_path):
            os.unlink(tmp_input_path)
        raise Exception(f"Error converting audio: {str(e)}")


def apply_lowpass_filter(waveform, sample_rate, cutoff_freq, order=5):
    """Apply a low-pass Butterworth filter."""
    nyquist = sample_rate / 2
    normalized_cutoff = cutoff_freq / nyquist
    
    if normalized_cutoff >= 1:
        return waveform  # Cutoff is too high, return original
    
    b, a = signal.butter(order, normalized_cutoff, btype='low', analog=False)
    filtered = signal.filtfilt(b, a, waveform)
    return filtered.astype(waveform.dtype)


def apply_highpass_filter(waveform, sample_rate, cutoff_freq, order=5):
    """Apply a high-pass Butterworth filter."""
    nyquist = sample_rate / 2
    normalized_cutoff = cutoff_freq / nyquist
    
    if normalized_cutoff <= 0:
        return waveform  # Cutoff is too low, return original
    
    b, a = signal.butter(order, normalized_cutoff, btype='high', analog=False)
    filtered = signal.filtfilt(b, a, waveform)
    return filtered.astype(waveform.dtype)


def apply_bandpass_filter(waveform, sample_rate, low_freq, high_freq, order=5):
    """Apply a band-pass Butterworth filter."""
    nyquist = sample_rate / 2
    low = low_freq / nyquist
    high = high_freq / nyquist
    
    if low <= 0:
        low = 0.001
    if high >= 1:
        high = 0.999
    if low >= high:
        return waveform
    
    b, a = signal.butter(order, [low, high], btype='band', analog=False)
    filtered = signal.filtfilt(b, a, waveform)
    return filtered.astype(waveform.dtype)


def detect_harmonics(waveform, sample_rate, num_harmonics=10):
    """
    Detect the fundamental frequency and harmonics.
    
    Returns a list of (frequency, magnitude_db) tuples.
    """
    # Compute FFT
    fft = np.fft.fft(waveform)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    magnitude = np.abs(fft)
    
    # Only positive frequencies
    positive_mask = freqs > 0
    freqs = freqs[positive_mask]
    magnitude = magnitude[positive_mask]
    
    # Find peaks
    peaks, properties = signal.find_peaks(magnitude, height=np.max(magnitude) * 0.01)
    
    if len(peaks) == 0:
        return []
    
    # Sort by magnitude
    peak_magnitudes = magnitude[peaks]
    sorted_indices = np.argsort(peak_magnitudes)[::-1]
    
    # Get top harmonics
    harmonics = []
    for i in sorted_indices[:num_harmonics]:
        freq = freqs[peaks[i]]
        mag_db = 20 * np.log10(peak_magnitudes[i] / np.max(magnitude) + 1e-10)
        harmonics.append({
            'frequency': freq,
            'magnitude_db': mag_db
        })
    
    return harmonics


def calculate_speed_of_sound(temperature_celsius=20, medium='air'):
    """
    Calculate speed of sound in different media.
    
    Args:
        temperature_celsius: Temperature in Celsius (for air/water)
        medium: 'air', 'water', 'steel', 'aluminum', 'glass'
    
    Returns:
        Speed of sound in m/s
    """
    if medium == 'air':
        # v = 331.3 * sqrt(1 + T/273.15)
        return 331.3 * np.sqrt(1 + temperature_celsius / 273.15)
    elif medium == 'water':
        # Approximate formula
        return 1403 + 4.7 * temperature_celsius
    elif medium == 'steel':
        return 5960  # m/s (approximately constant)
    elif medium == 'aluminum':
        return 6420  # m/s
    elif medium == 'glass':
        return 5640  # m/s
    else:
        return 343  # Default to air at 20°C


def generate_synthetic_wave(wave_type, frequency, duration, sample_rate=44100, amplitude=0.8):
    """
    Generate synthetic sound waves for educational purposes.
    
    Args:
        wave_type: 'sine', 'square', 'sawtooth', 'triangle'
        frequency: Frequency in Hz
        duration: Duration in seconds
        sample_rate: Samples per second
        amplitude: Wave amplitude (0 to 1)
    
    Returns:
        numpy array of the waveform
    """
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    
    if wave_type == 'sine':
        wave = np.sin(2 * np.pi * frequency * t)
    elif wave_type == 'square':
        wave = signal.square(2 * np.pi * frequency * t)
    elif wave_type == 'sawtooth':
        wave = signal.sawtooth(2 * np.pi * frequency * t)
    elif wave_type == 'triangle':
        wave = signal.sawtooth(2 * np.pi * frequency * t, width=0.5)
    else:
        wave = np.sin(2 * np.pi * frequency * t)
    
    # Normalize and apply amplitude
    wave = wave * amplitude
    
    # Convert to int16 for WAV compatibility
    wave_int16 = (wave * 32767).astype(np.int16)
    
    return wave_int16, sample_rate


def export_audio_to_wav_bytes(waveform, sample_rate):
    """
    Export waveform to WAV bytes for download.
    
    Returns: BytesIO object containing WAV data
    """
    buffer = io.BytesIO()
    wavfile.write(buffer, sample_rate, waveform)
    buffer.seek(0)
    return buffer


def export_analysis_to_csv(file_info, audio_levels, waveform, sample_rate):
    """
    Export analysis data to CSV format.
    
    Returns: CSV string
    """
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Metadata section
    writer.writerow(['=== FILE INFORMATION ==='])
    writer.writerow(['Property', 'Value'])
    writer.writerow(['Sample Rate (Hz)', file_info['sample_rate']])
    writer.writerow(['Duration (s)', f"{file_info['duration']:.4f}"])
    writer.writerow(['Channels', file_info['channels']])
    writer.writerow(['Channel Type', file_info['channel_type']])
    writer.writerow(['Total Samples', file_info['total_samples']])
    writer.writerow([])
    
    # Audio levels section
    writer.writerow(['=== AUDIO LEVELS ==='])
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Average dB', f"{audio_levels['avg_db']:.2f}"])
    writer.writerow(['RMS dB', f"{audio_levels['rms_db']:.2f}"])
    writer.writerow(['Max dB', f"{audio_levels['db_range']['max_db']:.2f}"])
    writer.writerow(['Min dB', f"{audio_levels['db_range']['min_db']:.2f}"])
    writer.writerow(['Dynamic Range (dB)', f"{audio_levels['db_range']['dynamic_range']:.2f}"])
    writer.writerow([])
    
    # Amplitude statistics
    writer.writerow(['=== AMPLITUDE STATISTICS ==='])
    writer.writerow(['Metric', 'Value'])
    writer.writerow(['Max Amplitude', np.max(waveform)])
    writer.writerow(['Min Amplitude', np.min(waveform)])
    writer.writerow(['Mean Amplitude', f"{np.mean(waveform):.2f}"])
    writer.writerow(['Std Deviation', f"{np.std(waveform):.2f}"])
    
    return output.getvalue()
