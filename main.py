import streamlit as st
from utils.styling import apply_custom_css
from utils.data_loader import load_session

from components.sidebar import render_sidebar
from components.track_map import render_track_map
from components.telemetry import render_telemetry_traces, render_strategy_charts
from components.lap_analysis import render_lap_analysis

# Page config
st.set_page_config(
    page_title="F1 Analytics Dashboard",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

# Render Sidebar
sidebar_data = render_sidebar()

# Main Layout
if sidebar_data and sidebar_data['session']:
    session = sidebar_data['session']
    year = sidebar_data['year']
    gp = sidebar_data['gp']
    session_type = sidebar_data['session_type']
    selected_drivers = sidebar_data['selected_drivers']
    selected_laps = sidebar_data['selected_laps']
    
    # Top Header
    st.title(f"{year} {gp} - {session_type}")
    
    # Split Layout
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        render_track_map(session, selected_drivers)
        render_strategy_charts(session, selected_drivers)
        
    with col_right:
        render_telemetry_traces(session, selected_drivers)
    
    # Full Width Section for Lap Analysis
    st.markdown("---")
    render_lap_analysis(session, selected_drivers)

else:
    st.info("Please select a session and click 'Load Session Data' to begin.")
    st.markdown("""
    ### Welcome to the F1 Analytics Dashboard
    
    Use the sidebar to select a race session. 
    
    **Features:**
    - 🗺️ **Interactive Track Map**: Visualize speed, gear, and braking zones.
    - 📈 **Telemetry Analysis**: Compare speed, throttle, and brake traces between drivers.
    - ⚔️ **Battle Analysis**: Track position changes and gaps.
    - 🛞 **Strategy Insights**: Tyre stints and lap time consistency.
    """)
