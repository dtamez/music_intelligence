import plotly.graph_objects as go


def plot_signal_and_rms(
    signal, rms_envelope, downsample_factor=200, hop_size=512, title="Signal + RMS"
):
    """
    Visual sanity check of our signal.
    """
    # Downsample signal for faster plotting
    signal_ds = signal[::downsample_factor]

    # Expand RMS envelope to roughly match downsampled signal
    energy_expanded = []
    for e in rms_envelope:
        energy_expanded.extend([e] * max(1, hop_size // downsample_factor))
    energy_expanded = energy_expanded[: len(signal_ds)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=signal_ds, mode="lines", name="Raw Signal"))
    fig.add_trace(
        go.Scatter(
            y=energy_expanded,
            mode="lines",
            name="RMS Envelope",
            line=dict(color="orange"),
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Sample (downsampled)",
        yaxis_title="Amplitude/Energy",
        legend=dict(x=0, y=1.0),
    )

    fig.show()
