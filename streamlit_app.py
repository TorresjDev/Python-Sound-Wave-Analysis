"""
Sound Wave Analysis - Streamlit Web Application

A professional web-based tool for analyzing and visualizing audio files.
Supports WAV, MP3, and FLAC formats with interactive visualizations.

Author: TorresjDev
License: CC BY-NC 4.0
"""

import streamlit as st
import numpy as np
import os
from datetime import datetime

# Import analysis modules
from sound_analysis.analyzer import get_wave_info, load_wave_data, analyze_audio_levels
from sound_analysis.plotly_viz import create_all_visualizations, create_frequency_spectrum_plot
from sound_analysis.audio_processing import (
    convert_audio_to_wav,
    detect_harmonics,
    calculate_speed_of_sound,
    export_analysis_to_csv,
    apply_lowpass_filter,
    apply_highpass_filter,
    apply_bandpass_filter,
    PYDUB_AVAILABLE
)

# Page configuration
st.set_page_config(
    page_title="Sound Wave Analysis",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for gradients and polish
# We rely on Streamlit's native Light/Dark modes for base colors
st.markdown("""
<style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    
    /* Gradient Text Header - Works on both backgrounds */
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header { text-align: center; opacity: 0.7; font-size: 1.1rem; margin-bottom: 2rem; }
    
    /* Info box styling - uses primary color with transparency */
    .info-box {
        background: rgba(99, 102, 241, 0.1);
        border-left: 4px solid #6366f1;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    
    /* Hide default menu elements we don't want */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    defaults = {
        'analysis_complete': False,
        'file_info': None,
        'audio_levels': None,
        'figures': None,
        'waveform': None,
        'sample_rate': None,
        'duration': None,
        'harmonics': None,
        'uploaded_filename': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar():
    """Render the sidebar with settings and tools."""
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        st.markdown("""
        **🎨 Theme:**  
        Use the app menu (**⋮**) ➜ **Settings** ➜ **Theme**
        to toggle Light/Dark mode.
        """)
        
        st.divider()
        
        # FFT Settings
        st.markdown("### 🔧 FFT Settings")
        
        fft_window = st.select_slider(
            "Window Size",
            options=[256, 512, 1024, 2048, 4096, 8192],
            value=1024,
            help="Larger = better frequency resolution, worse time resolution"
        )
        
        st.session_state['fft_window'] = fft_window
        
        st.divider()
        
        # Speed of Sound Calculator
        st.markdown("### 🔊 Speed of Sound")
        
        medium = st.selectbox(
            "Medium",
            ['air', 'water', 'steel', 'aluminum', 'glass']
        )
        
        temp = st.slider("Temperature (°C)", -20, 50, 20) if medium in ['air', 'water'] else 20
        
        speed = calculate_speed_of_sound(temp, medium)
        st.metric("Speed of Sound", f"{speed:.1f} m/s")
        
        st.divider()
        
        # About section
        st.markdown("### 📊 About")
        st.markdown("""
        **Sound Wave Analysis** - Professional audio analysis tool.
        
        **Supported formats:** WAV, MP3, FLAC  
        **Max file size:** 50MB
        """)
        
        if not PYDUB_AVAILABLE:
            st.warning("⚠️ MP3/FLAC support requires pydub. Install with: `pip install pydub`")
        
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.8rem; margin-top: 2rem;">
            Created by <b>TorresjDev</b><br>
            <a href="https://github.com/TorresjDev/Python-Sound-Wave-Analysis">GitHub</a>
        </div>
        """, unsafe_allow_html=True)


def render_header():
    """Render the main header."""
    st.markdown('<h1 class="main-header">🌊 Sound Wave Analysis</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Professional audio analysis and visualization tool</p>', unsafe_allow_html=True)


def render_upload_section():
    """Render the file upload section."""
    st.markdown("### 📁 Upload Audio File")
    
    # Determine supported formats
    formats = ['wav']
    if PYDUB_AVAILABLE:
        formats.extend(['mp3', 'flac'])
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        uploaded_file = st.file_uploader(
            "Drag and drop or click to upload",
            type=formats,
            help=f"Supported: {', '.join(f.upper() for f in formats)} (max 50MB)",
            label_visibility="collapsed"
        )
        
        format_str = ', '.join(f.upper() for f in formats)
        st.caption(f"📌 Supported formats: {format_str} | Maximum size: 50MB")
    
    return uploaded_file


def render_metrics(file_info, audio_levels):
    """Render the metrics cards."""
    st.markdown("### 📊 Analysis Results")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Sample Rate", f"{file_info['sample_rate']:,} Hz")
    with col2:
        st.metric("Duration", f"{file_info['duration']:.2f}s")
    with col3:
        st.metric("Channels", f"{file_info['channels']} ({file_info['channel_type']})")
    with col4:
        st.metric("Avg dB", f"{audio_levels['avg_db']:.1f}")
    with col5:
        st.metric("RMS dB", f"{audio_levels['rms_db']:.1f}")
    with col6:
        st.metric("Dynamic Range", f"{audio_levels['db_range']['dynamic_range']:.1f} dB")


def render_harmonics(harmonics):
    """Render harmonic analysis results."""
    if not harmonics:
        return
    
    st.markdown("### 🎵 Harmonic Analysis")
    st.caption("Detected frequency peaks (fundamental and overtones)")
    
    cols = st.columns(min(5, len(harmonics)))
    
    for i, harm in enumerate(harmonics[:5]):
        with cols[i]:
            freq_str = f"{harm['frequency']:.1f} Hz" if harm['frequency'] < 1000 else f"{harm['frequency']/1000:.2f} kHz"
            label = "Fundamental" if i == 0 else f"Harmonic {i}"
            st.metric(label, freq_str, f"{harm['magnitude_db']:.1f} dB")


def render_visualizations(figures):
    """Render all visualizations in a grid."""
    st.markdown("### 📈 Visualizations")
    st.markdown("*Hover for values • Click camera icon to download • Zoom/pan with mouse*")
    
    # Row 1: Waveform and Spectrum
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(figures['waveform'], use_container_width=True, key='waveform')
    with col2:
        st.plotly_chart(figures['spectrum'], use_container_width=True, key='spectrum')
    
    # Row 2: Spectrogram and PSD
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(figures['spectrogram'], use_container_width=True, key='spectrogram')
    with col4:
        st.plotly_chart(figures['psd'], use_container_width=True, key='psd')
    
    # Row 3: Phase and Histogram
    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(figures['phase'], use_container_width=True, key='phase')
    with col6:
        st.plotly_chart(figures['histogram'], use_container_width=True, key='histogram')


def analyze_audio(uploaded_file):
    """Analyze the uploaded audio file."""
    # Get file extension
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    
    # Convert to WAV if needed
    tmp_path = convert_audio_to_wav(uploaded_file, file_ext)
    
    try:
        # Get file info
        file_info = get_wave_info(tmp_path)
        
        # Load waveform data
        wave_data = load_wave_data(tmp_path)
        waveform = wave_data['waveform']
        sample_rate = wave_data['sample_rate']
        duration = wave_data['duration']
        
        # Analyze audio levels
        audio_levels = analyze_audio_levels(waveform)
        
        # Detect harmonics
        harmonics = detect_harmonics(waveform, sample_rate)
        
        # Generate visualizations
        figures = create_all_visualizations(
            waveform, sample_rate, duration, uploaded_file.name
        )
        
        return {
            'file_info': file_info,
            'audio_levels': audio_levels,
            'figures': figures,
            'waveform': waveform,
            'sample_rate': sample_rate,
            'duration': duration,
            'harmonics': harmonics,
            'wav_path': tmp_path
        }
        
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise e


def main():
    """Main application entry point."""
    init_session_state()
    render_sidebar()
    render_header()
    
    # File upload
    uploaded_file = render_upload_section()
    
    if uploaded_file is not None:
        # Check file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        if file_size_mb > 50:
            st.error(f"❌ File too large ({file_size_mb:.1f}MB). Maximum size is 50MB.")
            return
        
        # Show file info
        st.info(f"📄 **{uploaded_file.name}** ({file_size_mb:.2f} MB)")
        
        # Analyze button
        if st.button("🔬 Analyze Audio", type="primary", use_container_width=True):
            with st.spinner("Analyzing audio... This may take a moment for large files."):
                try:
                    results = analyze_audio(uploaded_file)
                    
                    # Store in session state
                    st.session_state.analysis_complete = True
                    st.session_state.file_info = results['file_info']
                    st.session_state.audio_levels = results['audio_levels']
                    st.session_state.figures = results['figures']
                    st.session_state.waveform = results['waveform']
                    st.session_state.sample_rate = results['sample_rate']
                    st.session_state.duration = results['duration']
                    st.session_state.harmonics = results['harmonics']
                    st.session_state.uploaded_filename = uploaded_file.name
                    
                    # Clean up temp file
                    if os.path.exists(results.get('wav_path', '')):
                        os.unlink(results['wav_path'])
                    
                    st.success("✅ Analysis complete!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error analyzing file: {str(e)}")
                    return
        
        # Show results if analysis is complete
        if st.session_state.analysis_complete:
            st.divider()
            
            # Audio Playback
            st.markdown("### 🔊 Audio Playback")
            st.audio(uploaded_file, format=f"audio/{os.path.splitext(uploaded_file.name)[1][1:]}")
            
            st.divider()
            
            # Export Options
            st.markdown("### 💾 Export Options")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # TXT Summary
                summary = f"""Sound Wave Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

File: {st.session_state.uploaded_filename}
Sample Rate: {st.session_state.file_info['sample_rate']:,} Hz
Duration: {st.session_state.file_info['duration']:.2f} seconds
Channels: {st.session_state.file_info['channels']} ({st.session_state.file_info['channel_type']})

Audio Levels:
- Average dB: {st.session_state.audio_levels['avg_db']:.2f}
- RMS dB: {st.session_state.audio_levels['rms_db']:.2f}
- Max dB: {st.session_state.audio_levels['db_range']['max_db']:.2f}
- Min dB: {st.session_state.audio_levels['db_range']['min_db']:.2f}
- Dynamic Range: {st.session_state.audio_levels['db_range']['dynamic_range']:.2f} dB

Harmonics Detected:
"""
                for i, h in enumerate(st.session_state.harmonics[:5]):
                    label = "Fundamental" if i == 0 else f"Harmonic {i}"
                    summary += f"- {label}: {h['frequency']:.1f} Hz ({h['magnitude_db']:.1f} dB)\n"
                
                st.download_button(
                    "📄 Summary (TXT)",
                    data=summary,
                    file_name=f"analysis_{st.session_state.uploaded_filename.replace('.', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                # CSV Export
                csv_data = export_analysis_to_csv(
                    st.session_state.file_info,
                    st.session_state.audio_levels,
                    st.session_state.waveform,
                    st.session_state.sample_rate
                )
                st.download_button(
                    "📊 Data (CSV)",
                    data=csv_data,
                    file_name=f"analysis_{st.session_state.uploaded_filename.replace('.', '_')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col3:
                st.markdown("**📷 Graphs:**")
                st.caption("Click camera icon on graphs")
            
            with col4:
                st.caption("📄 PDF export coming soon!")
            
            st.divider()
            
            # Analysis Results
            render_metrics(st.session_state.file_info, st.session_state.audio_levels)
            
            st.divider()
            
            # Harmonic Analysis
            render_harmonics(st.session_state.harmonics)
            
            st.divider()
            
            # Visualizations
            render_visualizations(st.session_state.figures)
            
            # Educational section
            st.divider()
            st.markdown("### 📚 Physics Reference")
            
            with st.expander("Wave Equations & Formulas"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Wave Equation:**")
                    st.latex(r"y(x,t) = A \sin(kx - \omega t + \phi)")
                    
                    st.markdown("**Frequency & Period:**")
                    st.latex(r"f = \frac{1}{T}, \quad \omega = 2\pi f")
                    
                with col2:
                    st.markdown("**Speed of Sound:**")
                    st.latex(r"v = 331.3 \sqrt{1 + \frac{T}{273.15}} \, \text{m/s}")
                    
                    st.markdown("**Decibel Level:**")
                    st.latex(r"L_{dB} = 20 \log_{10}\left(\frac{A}{A_{ref}}\right)")
    
    else:
        # Welcome message
        st.markdown("""
        <div class="info-box">
            <b>👋 Welcome!</b><br>
            Upload an audio file above to get started with your analysis.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🎯 Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **📊 6 Professional Graphs**
            - Waveform
            - Frequency Spectrum
            - Spectrogram
            - Power Spectral Density
            - Phase Response
            - Amplitude Histogram
            """)
        
        with col2:
            st.markdown("""
            **🔬 Detailed Analysis**
            - Sample rate & duration
            - dB levels & dynamic range
            - Harmonic detection
            - Physics calculators
            """)
        
        with col3:
            st.markdown("""
            **💾 Export Options**
            - Download graphs (PNG)
            - Export summary (TXT)
            - Export data (CSV)
            - Audio playback
            """)


if __name__ == "__main__":
    main()
