import streamlit as st
import plotly.graph_objects as go
from utils.data_loader import load_laps

from plotly.subplots import make_subplots

def render_telemetry_traces(session, selected_drivers):
    """
    Render telemetry traces for selected drivers (Speed, RPM/Gear, Throttle/Brake).
    """
    st.markdown("### 📈 Telemetry Traces")
    
    if not selected_drivers:
        st.warning("Select drivers to compare telemetry.")
        return

    with st.spinner("Generating telemetry traces..."):
        try:
            # Create subplots: Speed, RPM/Gear, Throttle/Brake
            fig = make_subplots(
                rows=3, cols=1, 
                shared_xaxes=True,
                vertical_spacing=0.05,
                subplot_titles=("Speed", "RPM & Gear", "Throttle & Brake")
            )
            
            for driver in selected_drivers:
                lap = session.laps.pick_drivers(driver).pick_fastest()
                if lap is None:
                    continue
                tel = lap.get_telemetry()
                
                # Speed Trace
                fig.add_trace(
                    go.Scatter(x=tel['Distance'], y=tel['Speed'], mode='lines', name=f"{driver} Speed"),
                    row=1, col=1
                )
                
                # RPM Trace
                fig.add_trace(
                    go.Scatter(x=tel['Distance'], y=tel['RPM'], mode='lines', name=f"{driver} RPM", opacity=0.7),
                    row=2, col=1
                )
                
                # Gear Trace (Secondary Y-axis logic is complex in subplots, so we might just overlay or use a separate chart if needed. 
                # For now, let's just show RPM. Gear is discrete and might clutter.)
                # Alternatively, we can scale Gear to fit or just show it on hover. 
                # Let's add Gear as a separate step line if requested, but RPM is usually more useful for "traces".
                # PRD asks for "Y-Axis 2 (RPM/Gear)". Let's try to add Gear on a secondary axis if possible, 
                # but for simplicity in this grid, let's stick to RPM and maybe add Gear as text or color?
                # Actually, let's just plot Gear on the same row but maybe scaled or just let the user toggle.
                # Let's stick to RPM for now to keep it clean, or add Gear as a separate trace.
                
                # Throttle & Brake
                fig.add_trace(
                    go.Scatter(x=tel['Distance'], y=tel['Throttle'], mode='lines', name=f"{driver} Throttle", line=dict(dash='solid')),
                    row=3, col=1
                )
                fig.add_trace(
                    go.Scatter(x=tel['Distance'], y=tel['Brake'] * 100, mode='lines', name=f"{driver} Brake", line=dict(dash='dot')),
                    row=3, col=1
                )

            fig.update_layout(
                height=800,
                template="plotly_dark",
                hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            fig.update_yaxes(title_text="Speed (km/h)", row=1, col=1)
            fig.update_yaxes(title_text="RPM", row=2, col=1)
            fig.update_yaxes(title_text="Input (%)", row=3, col=1)
            fig.update_xaxes(title_text="Distance (m)", row=3, col=1)
            
            st.plotly_chart(fig, width="stretch")
            
        except Exception as e:
            st.error(f"Error generating telemetry: {e}")

def render_strategy_charts(session, selected_drivers):
    """
    Deprecated: Use components.strategy.render_strategy_charts instead.
    """
    pass
