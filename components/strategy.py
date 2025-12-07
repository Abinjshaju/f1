import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def render_strategy_charts(session, selected_drivers):
    """
    Render strategy charts: Tyre Stint History and Lap Time Distribution.
    """
    st.markdown("### 🛞 Strategy & Pace")
    
    if not selected_drivers:
        st.warning("Select drivers to analyze strategy.")
        return

    tab1, tab2 = st.tabs(["📊 Tyre Stints", "⏱️ Lap Time Distribution"])
    
    with tab1:
        render_tyre_stints(session, selected_drivers)
        
    with tab2:
        render_lap_time_distribution(session, selected_drivers)

def render_tyre_stints(session, selected_drivers):
    """
    Render a horizontal bar chart showing tyre stints.
    """
    try:
        laps = session.laps
        drivers_laps = laps[laps['Driver'].isin(selected_drivers)].copy()
        
        # Group by Driver and Stint to get start and end laps
        stints = drivers_laps.groupby(['Driver', 'Stint', 'Compound']).agg(
            StartLap=('LapNumber', 'min'),
            EndLap=('LapNumber', 'max'),
            LapsRun=('LapNumber', 'count')
        ).reset_index()
        
        # Color map for tyres
        tyre_colors = {
            'SOFT': '#FF3333',
            'MEDIUM': '#FFFF33',
            'HARD': '#E0E0E0',
            'INTERMEDIATE': '#39B54A',
            'WET': '#00AEEF',
            'UNKNOWN': '#808080'
        }
        
        fig = px.timeline(
            stints, 
            x_start="StartLap", 
            x_end="EndLap", 
            y="Driver", 
            color="Compound",
            color_discrete_map=tyre_colors,
            hover_data=['LapsRun'],
            title="Tyre Stint History"
        )
        
        fig.update_yaxes(categoryorder="total ascending")
        fig.update_layout(
            xaxis_title="Lap Number",
            yaxis_title="Driver",
            template="plotly_dark",
            height=300 + (len(selected_drivers) * 20),
            showlegend=True
        )
        
        st.plotly_chart(fig, width="stretch")
        
    except Exception as e:
        st.error(f"Error generating tyre stints: {e}")

def render_lap_time_distribution(session, selected_drivers):
    """
    Render a box plot of lap times to show consistency.
    """
    try:
        laps = session.laps
        drivers_laps = laps[laps['Driver'].isin(selected_drivers)].copy()
        
        # Filter out slow laps (e.g., pit stops, safety car) for better visualization
        # Using 107% rule or just a reasonable cutoff like 1.1 * median
        # For simplicity, let's just remove outliers > 1.2 * fastest lap of the session
        fastest_lap = laps.pick_fastest()['LapTime'].total_seconds()
        threshold = fastest_lap * 1.15
        
        drivers_laps['LapTimeSeconds'] = drivers_laps['LapTime'].dt.total_seconds()
        clean_laps = drivers_laps[drivers_laps['LapTimeSeconds'] < threshold]
        
        fig = px.box(
            clean_laps, 
            x="Driver", 
            y="LapTimeSeconds", 
            color="Driver",
            title="Lap Time Distribution (Clean Laps)",
            points="all"
        )
        
        fig.update_layout(
            yaxis_title="Lap Time (s)",
            template="plotly_dark",
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, width="stretch")
        
    except Exception as e:
        st.error(f"Error generating lap time distribution: {e}")
