import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from utils.data_loader import load_laps

def render_track_map(session, selected_drivers, color_by='Speed'):
    """
    Render the track map colored by a specific telemetry channel.
    """
    st.markdown("### 📍 Telemetry Track Map")
    
    # Controls for the map
    col1, col2 = st.columns([1, 1])
    with col1:
        color_option = st.selectbox("Color Track By", ['Speed', 'nGear', 'Brake'], index=0)
    
    with col2:
        driver_for_map = st.selectbox("Select Driver for Map", selected_drivers, index=0)

    if not driver_for_map:
        st.warning("Please select a driver to generate the map.")
        return

    with st.spinner(f"Generating track map for {driver_for_map}..."):
        try:
            lap = session.laps.pick_drivers(driver_for_map).pick_fastest()
            if lap is None:
                st.warning(f"No fastest lap data available for {driver_for_map}.")
                return
                
            tel = lap.get_telemetry()
            
            # Create the plot
            if color_option == 'Speed':
                fig = px.scatter(tel, x='X', y='Y', color='Speed', title=f"{driver_for_map} - Speed", color_continuous_scale='Viridis')
            elif color_option == 'nGear':
                fig = px.scatter(tel, x='X', y='Y', color='nGear', title=f"{driver_for_map} - Gear", color_continuous_scale='RdBu')
            elif color_option == 'Brake':
                fig = px.scatter(tel, x='X', y='Y', color='Brake', title=f"{driver_for_map} - Brake", color_discrete_map={0: 'gray', 1: 'red'})
            
            # Add Corner Annotations
            circuit_info = session.get_circuit_info()
            if circuit_info is not None:
                corners = circuit_info.corners
                # Create a scatter trace for corners
                fig.add_trace(go.Scatter(
                    x=corners['X'], 
                    y=corners['Y'], 
                    mode='text', 
                    text=corners['Number'].astype(str),
                    textposition="top center",
                    textfont=dict(size=10, color="white"),
                    name="Corners",
                    hoverinfo='skip'
                ))
            
            # Style the plot to look like a track map
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, visible=False),
                yaxis=dict(showgrid=False, zeroline=False, visible=False, scaleanchor="x", scaleratio=1),
                margin=dict(l=0, r=0, t=30, b=0),
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, width="stretch")
            
        except Exception as e:
            st.error(f"Error generating track map: {e}")
