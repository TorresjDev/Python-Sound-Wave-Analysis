#!/usr/bin/env python3
"""
Sound Wave Analysis - Clean and Modular

A user-friendly tool for analyzing WAV files with visualization.

Author: TorresjDev
License: MIT
"""

import os
from sound_analysis.analyzer import perform_complete_analysis
from sound_analysis.tools import select_wav_file, get_analysis_options


def main():
    """Main function - clean and modular."""
    print("🌊 Welcome to Sound Wave Analysis!")
    print("=" * 40)
    
    # Let user select a WAV file
    selected_file = select_wav_file()
    
    if selected_file:
        print(f"\n🎯 Analyzing: {os.path.basename(selected_file)}")
        
        # Get analysis options
        options = get_analysis_options()
        
        # Perform analysis using the analyzer module
        perform_complete_analysis(
            selected_file, 
            show_plots=options["show_plots"],
            save_figures=options["save_figures"]
        )
    else:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
