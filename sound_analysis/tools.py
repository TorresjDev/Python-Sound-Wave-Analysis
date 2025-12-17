"""
Sound Analysis Tools

Mathematical functions for audio processing and analysis.
File management and user interface utilities.
"""

import os
import numpy as np


def wave_to_db(waveform):
    """Convert waveform to decibels."""
    sq_amplitude = waveform ** 2
    mean_squared_amplitude = np.mean(sq_amplitude)
    decibels = 10 * np.log10(mean_squared_amplitude / 1e-6)
    return decibels


def wave_to_db_rms(waveform):
    """Convert waveform to decibels using RMS."""
    sq_amplitude = np.mean(waveform ** 2)
    rms_value = np.sqrt(sq_amplitude)
    decibels = 20 * np.log10(rms_value / 1e-6)
    return decibels


def detect_db_range(waveform):
    """Detect the dynamic range of the audio in decibels."""
    max_amplitude = np.max(np.abs(waveform))
    min_amplitude = np.min(np.abs(waveform[waveform != 0]))  # Avoid log(0)
    
    max_db = 20 * np.log10(max_amplitude / 1e-6) if max_amplitude > 0 else -np.inf
    min_db = 20 * np.log10(min_amplitude / 1e-6) if min_amplitude > 0 else -np.inf
    
    dynamic_range = max_db - min_db if min_db != -np.inf else 0
    
    return {
        'max_db': max_db,
        'min_db': min_db,
        'dynamic_range': dynamic_range
    }


def normalize_waveform(waveform):
    """Normalize waveform to [-1, 1] range."""
    max_val = np.max(np.abs(waveform))
    if max_val > 0:
        return waveform / max_val
    return waveform


def list_wav_files():
    """List all WAV files in the data directory."""
    data_dir = "data"
    wav_files = []
    
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.lower().endswith('.wav'):
                wav_files.append(file)
    
    return wav_files


def select_wav_file():
    """Let user select a WAV file with arrow key navigation."""
    try:
        import keyboard
        keyboard_available = True
    except ImportError:
        keyboard_available = False
        
    wav_files = list_wav_files()
    
    if not wav_files:
        print("❌ No WAV files found in the 'data' directory!")
        print("📁 Please add some .wav files to the 'data' folder and try again.")
        return None
    
    if not keyboard_available:
        # Fallback to number selection if keyboard module not available
        print("🎵 Available WAV files:")
        print("=" * 30)
        
        for i, file in enumerate(wav_files, 1):
            print(f"{i}. {file}")
        
        while True:
            try:
                choice = input(f"\n📂 Select a file (1-{len(wav_files)}) or 'q' to quit: ").strip()
                
                if choice.lower() == 'q':
                    return None
                    
                choice_num = int(choice)
                if 1 <= choice_num <= len(wav_files):
                    selected_file = wav_files[choice_num - 1]
                    return os.path.join("data", selected_file)
                else:
                    print(f"❌ Please enter a number between 1 and {len(wav_files)}")
                    
            except ValueError:
                print("❌ Please enter a valid number or 'q' to quit")
    else:
        # Enhanced UX with arrow key navigation
        selected_index = 0
        
        def display_menu():
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
            print("🎵 Available WAV files:")
            print("=" * 50)
            print("Use ↑/↓ arrows to navigate, Enter to select, 'q' to quit")
            print("=" * 50)
            
            for i, file in enumerate(wav_files):
                if i == selected_index:
                    print(f"► {file} ◄")  # Highlight selected file
                else:
                    print(f"  {file}")
            
            print("\n" + "=" * 50)
            print(f"Selected: {wav_files[selected_index]}")
        
        display_menu()
        
        while True:
            try:
                event = keyboard.read_event()
                
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'up':
                        selected_index = (selected_index - 1) % len(wav_files)
                        display_menu()
                    elif event.name == 'down':
                        selected_index = (selected_index + 1) % len(wav_files)
                        display_menu()
                    elif event.name == 'enter':
                        selected_file = wav_files[selected_index]
                        print(f"\n✅ Selected: {selected_file}")
                        return os.path.join("data", selected_file)
                    elif event.name == 'q':
                        return None
                    elif event.name == 'esc':
                        return None
                        
            except KeyboardInterrupt:
                return None


def get_analysis_options():
    """Get user preferences for analysis options."""
    try:
        import keyboard
        keyboard_available = True
    except ImportError:
        keyboard_available = False
    
    options_list = [
        {"name": "Standard analysis (waveform + spectrogram)", "show_plots": True, "save_figures": False},
        {"name": "Save figures to files", "show_plots": True, "save_figures": True},
        {"name": "Analysis only (no plots)", "show_plots": False, "save_figures": False}
    ]
    
    if not keyboard_available:
        # Fallback to number selection
        print("\n🔧 Analysis Options:")
        for i, option in enumerate(options_list, 1):
            print(f"{i}. {option['name']}")
        
        while True:
            try:
                choice = input("\n📊 Select option (1-3) or press Enter for default: ").strip()
                
                if choice == "" or choice == "1":
                    return options_list[0]
                elif choice == "2":
                    return options_list[1]
                elif choice == "3":
                    return options_list[2]
                else:
                    print("❌ Please enter 1, 2, or 3")
                    
            except ValueError:
                print("❌ Please enter a valid option")
    else:
        # Enhanced UX with arrow key navigation
        selected_index = 0
        
        def display_options_menu():
            os.system('cls' if os.name == 'nt' else 'clear')
            print("🔧 Analysis Options:")
            print("=" * 50)
            print("Use ↑/↓ arrows to navigate, Enter to select")
            print("=" * 50)
            
            for i, option in enumerate(options_list):
                if i == selected_index:
                    print(f"► {option['name']} ◄")
                else:
                    print(f"  {option['name']}")
            
            print("\n" + "=" * 50)
            print(f"Selected: {options_list[selected_index]['name']}")
        
        display_options_menu()
        
        while True:
            try:
                event = keyboard.read_event()
                
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == 'up':
                        selected_index = (selected_index - 1) % len(options_list)
                        display_options_menu()
                    elif event.name == 'down':
                        selected_index = (selected_index + 1) % len(options_list)
                        display_options_menu()
                    elif event.name == 'enter':
                        selected_option = options_list[selected_index]
                        print(f"\n✅ Selected: {selected_option['name']}")
                        return selected_option
                    elif event.name == 'esc':
                        return options_list[0]  # Default option
                        
            except KeyboardInterrupt:
                return options_list[0]  # Default option
