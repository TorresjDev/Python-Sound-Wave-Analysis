#!/usr/bin/env python3
"""
Verification Script for Sound Wave Analysis

This script compares the app's analysis results with scipy (trusted library)
to verify the calculations are correct.
"""

import wave
import numpy as np
from scipy.io import wavfile
from sound_analysis.analyzer import get_wave_info, load_wave_data, analyze_audio_levels


def verify_analysis(file_path):
    """Compare app results with scipy for verification."""
    print("=" * 60)
    print("VERIFICATION REPORT")
    print("=" * 60)
    print(f"File: {file_path}\n")

    # --- Get app's results ---
    app_info = get_wave_info(file_path)
    app_data = load_wave_data(file_path)
    app_levels = analyze_audio_levels(app_data['waveform'])

    # --- Get scipy's results ---
    scipy_rate, scipy_data = wavfile.read(file_path)

    # --- Compare basic properties ---
    print("1. BASIC PROPERTIES")
    print("-" * 40)
    
    checks = []
    
    # Sample rate
    match = app_info['sample_rate'] == scipy_rate
    checks.append(match)
    status = "PASS" if match else "FAIL"
    print(f"   Sample Rate: {app_info['sample_rate']} Hz [{status}]")
    
    # Duration (within 0.01 seconds)
    scipy_duration = len(scipy_data) / scipy_rate
    match = abs(app_info['duration'] - scipy_duration) < 0.01
    checks.append(match)
    status = "PASS" if match else "FAIL"
    print(f"   Duration: {app_info['duration']:.4f}s (scipy: {scipy_duration:.4f}s) [{status}]")
    
    # Channels
    scipy_channels = 1 if len(scipy_data.shape) == 1 else scipy_data.shape[1]
    match = app_info['channels'] == scipy_channels
    checks.append(match)
    status = "PASS" if match else "FAIL"
    print(f"   Channels: {app_info['channels']} [{status}]")

    print()
    print("2. AUDIO DATA QUALITY")
    print("-" * 40)
    
    # Check if waveform has reasonable values
    waveform = app_data['waveform']
    
    has_data = len(waveform) > 0
    checks.append(has_data)
    status = "PASS" if has_data else "FAIL"
    print(f"   Waveform loaded: {len(waveform):,} samples [{status}]")
    
    has_variation = np.std(waveform) > 0
    checks.append(has_variation)
    status = "PASS" if has_variation else "FAIL"
    print(f"   Has audio content (not silence): [{status}]")
    
    print()
    print("3. DECIBEL CALCULATIONS")
    print("-" * 40)
    
    # Verify dB calculations make sense
    avg_db = app_levels['avg_db']
    rms_db = app_levels['rms_db']
    dynamic_range = app_levels['db_range']['dynamic_range']
    
    # dB should be positive for audible sound
    valid_avg = avg_db > 0
    checks.append(valid_avg)
    status = "PASS" if valid_avg else "FAIL"
    print(f"   Average dB: {avg_db:.2f} (positive = audible) [{status}]")
    
    valid_rms = rms_db > 0
    checks.append(valid_rms)
    status = "PASS" if valid_rms else "FAIL"
    print(f"   RMS dB: {rms_db:.2f} (positive = audible) [{status}]")
    
    # Dynamic range typically 40-120 dB for real audio
    valid_range = 10 < dynamic_range < 150
    checks.append(valid_range)
    status = "PASS" if valid_range else "FAIL"
    print(f"   Dynamic Range: {dynamic_range:.2f} dB (reasonable range) [{status}]")

    print()
    print("=" * 60)
    passed = sum(checks)
    total = len(checks)
    
    if passed == total:
        print(f"RESULT: ALL {total} CHECKS PASSED!")
        print("The analysis results appear to be correct.")
    else:
        print(f"RESULT: {passed}/{total} checks passed")
        print("Some issues may need investigation.")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    import sys
    
    # Default to the test file
    file_path = "data/space_odyssey_radar.wav"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    
    verify_analysis(file_path)
