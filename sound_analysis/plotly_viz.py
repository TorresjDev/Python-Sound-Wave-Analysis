"""
Professional Plotly Visualizations for Sound Wave Analysis

Publication-quality interactive graphs for physics professionals.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal


# Professional color scheme
COLORS = {
    'primary': '#6366f1',      # Indigo
    'secondary': '#8b5cf6',    # Purple
    'accent': '#06b6d4',       # Cyan
    'warning': '#f59e0b',      # Amber
    'success': '#10b981',      # Emerald
    'background': '#1e1e2e',
    'grid': 'rgba(255,255,255,0.1)',
    'text': '#fafafa'
}

# Common layout settings for professional appearance
LAYOUT_DEFAULTS = {
    'template': 'plotly_dark',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'family': 'Inter, sans-serif', 'size': 12, 'color': COLORS['text']},
    'margin': {'l': 60, 'r': 40, 't': 50, 'b': 50},
    'hovermode': 'x unified'
}


def create_waveform_plot(waveform, sample_rate, duration, title="Waveform"):
    """
    Create an interactive waveform plot.
    
    Shows amplitude over time - useful for identifying:
    - Transients and attack characteristics
    - Envelope shape
    - Clipping
    """
    time = np.linspace(0, duration, num=len(waveform))
    
    # Downsample for performance if too many points
    max_points = 50000
    if len(waveform) > max_points:
        step = len(waveform) // max_points
        time = time[::step]
        waveform = waveform[::step]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time,
        y=waveform,
        mode='lines',
        line=dict(color=COLORS['primary'], width=0.5),
        name='Amplitude',
        hovertemplate='Time: %{x:.4f}s<br>Amplitude: %{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f'<b>{title}</b>', font=dict(size=16)),
        xaxis=dict(
            title='Time (seconds)',
            gridcolor=COLORS['grid'],
            showgrid=True,
            zeroline=True,
            zerolinecolor=COLORS['grid']
        ),
        yaxis=dict(
            title='Amplitude',
            gridcolor=COLORS['grid'],
            showgrid=True,
            zeroline=True,
            zerolinecolor=COLORS['accent']
        ),
        **LAYOUT_DEFAULTS
    )
    
    return fig


def create_frequency_spectrum_plot(waveform, sample_rate, title="Frequency Spectrum"):
    """
    Create a frequency spectrum plot styled like Audacity's Frequency Analysis.
    
    Shows magnitude in dB vs frequency on a log scale.
    Matches Audacity's display with clear dB and Hz labels.
    """
    # Compute FFT
    fft = np.fft.fft(waveform)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    magnitude = np.abs(fft)
    
    # Only positive frequencies
    positive_mask = freqs > 0
    freqs = freqs[positive_mask]
    magnitude = magnitude[positive_mask]
    
    # Convert to dB (relative to max, like Audacity)
    magnitude_db = 20 * np.log10(magnitude / magnitude.max() + 1e-10)
    
    # Smooth for cleaner display (like Audacity's smoothing)
    if len(magnitude_db) > 2000:
        window_size = len(magnitude_db) // 1000
        magnitude_db = np.convolve(magnitude_db, np.ones(window_size)/window_size, mode='same')
    
    fig = go.Figure()
    
    # Filled area plot like Audacity
    fig.add_trace(go.Scatter(
        x=freqs,
        y=magnitude_db,
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(138, 43, 226, 0.5)',  # Purple like Audacity
        line=dict(color='#8B2BE2', width=1),
        name='Level',
        hovertemplate='<b>%{x:.1f} Hz</b><br>%{y:.1f} dB<extra></extra>'
    ))
    
    # Create frequency tick values for log scale (like Audacity)
    freq_ticks = [20, 50, 100, 200, 500, 1000, 2000, 5000]
    max_freq = sample_rate / 2
    freq_ticks = [f for f in freq_ticks if f <= max_freq]
    
    # Create dB tick values (like Audacity: -60 to 0 in steps of 6)
    db_ticks = list(range(-60, 6, 6))
    
    fig.update_layout(
        title=dict(
            text=f'<b>{title}</b><br><span style="font-size:12px;color:#888">Frequency Analysis (like Audacity)</span>',
            font=dict(size=16)
        ),
        xaxis=dict(
            title=dict(text='<b>Frequency (Hz)</b>', font=dict(size=14)),
            type='log',
            gridcolor='rgba(255,255,255,0.2)',
            showgrid=True,
            gridwidth=1,
            tickvals=freq_ticks,
            ticktext=[f'{f} Hz' if f < 1000 else f'{f//1000}k Hz' for f in freq_ticks],
            tickfont=dict(size=11),
            range=[np.log10(20), np.log10(max_freq)],
            dtick=None,
            minor=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
        ),
        yaxis=dict(
            title=dict(text='<b>Level (dB)</b>', font=dict(size=14)),
            gridcolor='rgba(255,255,255,0.2)',
            showgrid=True,
            gridwidth=1,
            tickvals=db_ticks,
            ticktext=[f'{db} dB' for db in db_ticks],
            tickfont=dict(size=11),
            range=[-66, 3],
            zeroline=True,
            zerolinecolor='rgba(255,255,255,0.4)',
            zerolinewidth=2
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(30,30,46,0.8)',
        font={'family': 'Inter, sans-serif', 'size': 12, 'color': '#fafafa'},
        margin={'l': 70, 'r': 40, 't': 70, 'b': 60},
        hovermode='x unified'
    )
    
    return fig


def create_spectrogram_plot(waveform, sample_rate, title="Spectrogram"):
    """
    Create a time-frequency spectrogram.
    
    Shows how frequency content evolves over time.
    Useful for:
    - Tracking pitch changes
    - Identifying frequency modulation
    - Visualizing speech/music structure
    """
    # Compute spectrogram
    nperseg = min(1024, len(waveform) // 8)
    frequencies, times, Sxx = signal.spectrogram(
        waveform, 
        fs=sample_rate, 
        nperseg=nperseg,
        noverlap=nperseg // 2
    )
    
    # Convert to dB
    Sxx_db = 10 * np.log10(Sxx + 1e-10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Heatmap(
        x=times,
        y=frequencies,
        z=Sxx_db,
        colorscale='Viridis',
        colorbar=dict(title='dB', title_side='right'),
        hovertemplate='Time: %{x:.3f}s<br>Freq: %{y:.0f} Hz<br>Power: %{z:.1f} dB<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f'<b>{title}</b>', font=dict(size=16)),
        xaxis=dict(
            title='Time (seconds)',
            gridcolor=COLORS['grid']
        ),
        yaxis=dict(
            title='Frequency (Hz)',
            gridcolor=COLORS['grid'],
            range=[0, min(8000, sample_rate/2)]  # Cap at 8kHz for visibility
        ),
        **LAYOUT_DEFAULTS
    )
    
    return fig


def create_psd_plot(waveform, sample_rate, title="Power Spectral Density"):
    """
    Create a Power Spectral Density plot.
    
    Shows power distribution across frequencies.
    Useful for:
    - Energy analysis
    - Noise characterization
    - Comparing signal strengths
    """
    frequencies, psd = signal.welch(waveform, fs=sample_rate, nperseg=min(1024, len(waveform)//4))
    
    # Convert to dB
    psd_db = 10 * np.log10(psd + 1e-10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=frequencies,
        y=psd_db,
        mode='lines',
        fill='tozeroy',
        fillcolor='rgba(6, 182, 212, 0.3)',
        line=dict(color=COLORS['accent'], width=1.5),
        name='PSD',
        hovertemplate='Frequency: %{x:.1f} Hz<br>Power: %{y:.1f} dB/Hz<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f'<b>{title}</b>', font=dict(size=16)),
        xaxis=dict(
            title='Frequency (Hz)',
            type='log',
            gridcolor=COLORS['grid'],
            showgrid=True
        ),
        yaxis=dict(
            title='Power/Frequency (dB/Hz)',
            gridcolor=COLORS['grid'],
            showgrid=True
        ),
        **LAYOUT_DEFAULTS
    )
    
    return fig


def create_phase_plot(waveform, sample_rate, title="Phase Response"):
    """
    Create a phase response plot.
    
    Shows phase angle vs frequency.
    Useful for:
    - Phase relationship analysis
    - Filter characterization
    - Signal processing validation
    """
    fft = np.fft.fft(waveform)
    freqs = np.fft.fftfreq(len(fft), 1/sample_rate)
    phase = np.angle(fft, deg=True)
    
    # Only positive frequencies
    positive_mask = freqs > 0
    freqs = freqs[positive_mask]
    phase = phase[positive_mask]
    
    # Subsample for performance
    if len(freqs) > 5000:
        step = len(freqs) // 5000
        freqs = freqs[::step]
        phase = phase[::step]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=freqs,
        y=phase,
        mode='markers',
        marker=dict(color=COLORS['secondary'], size=2, opacity=0.5),
        name='Phase',
        hovertemplate='Frequency: %{x:.1f} Hz<br>Phase: %{y:.1f}°<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f'<b>{title}</b>', font=dict(size=16)),
        xaxis=dict(
            title='Frequency (Hz)',
            type='log',
            gridcolor=COLORS['grid'],
            showgrid=True
        ),
        yaxis=dict(
            title='Phase (degrees)',
            gridcolor=COLORS['grid'],
            showgrid=True,
            range=[-180, 180]
        ),
        **LAYOUT_DEFAULTS
    )
    
    return fig


def create_histogram_plot(waveform, title="Amplitude Distribution"):
    """
    Create an amplitude distribution histogram.
    
    Shows the distribution of amplitude values.
    Useful for:
    - Dynamic range analysis
    - Clipping detection
    - Signal statistics
    """
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=waveform,
        nbinsx=100,
        marker=dict(
            color=COLORS['success'],
            line=dict(color=COLORS['text'], width=0.5)
        ),
        opacity=0.8,
        name='Distribution',
        hovertemplate='Amplitude: %{x:,.0f}<br>Count: %{y:,}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=f'<b>{title}</b>', font=dict(size=16)),
        xaxis=dict(
            title='Amplitude',
            gridcolor=COLORS['grid'],
            showgrid=True
        ),
        yaxis=dict(
            title='Count',
            gridcolor=COLORS['grid'],
            showgrid=True
        ),
        **LAYOUT_DEFAULTS
    )
    
    return fig


def create_all_visualizations(waveform, sample_rate, duration, filename="Audio"):
    """
    Generate all 6 professional visualizations.
    
    Returns a dictionary of Plotly figures.
    """
    return {
        'waveform': create_waveform_plot(
            waveform, sample_rate, duration, 
            f"Waveform - {filename}"
        ),
        'spectrum': create_frequency_spectrum_plot(
            waveform, sample_rate,
            f"Frequency Spectrum - {filename}"
        ),
        'spectrogram': create_spectrogram_plot(
            waveform, sample_rate,
            f"Spectrogram - {filename}"
        ),
        'psd': create_psd_plot(
            waveform, sample_rate,
            f"Power Spectral Density - {filename}"
        ),
        'phase': create_phase_plot(
            waveform, sample_rate,
            f"Phase Response - {filename}"
        ),
        'histogram': create_histogram_plot(
            waveform,
            f"Amplitude Distribution - {filename}"
        )
    }
