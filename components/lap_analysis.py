import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def render_lap_analysis(session, selected_drivers):
    """
    Render lap analysis charts (Position Changes, Lap Times).
    """
    st.markdown("### 🏁 Race Progression & Laps")
    
    tab1, tab2, tab3 = st.tabs(["📈 Position Chart", "⚔️ Gap Analysis", "⏱️ Lap Data"])
    
    with tab1:
        render_position_chart(session, selected_drivers)
        
    with tab2:
        render_gap_analysis(session, selected_drivers)
        
    with tab3:
        render_lap_data_table(session, selected_drivers)

def render_gap_analysis(session, selected_drivers):
    """
    Render gap analysis (time delta) between drivers.
    """
    if len(selected_drivers) < 2:
        st.info("Select at least two drivers to compare gaps.")
        return
        
    with st.spinner("Calculating gaps..."):
        try:
            # Reference driver is the first selected driver
            ref_driver = selected_drivers[0]
            others = selected_drivers[1:]
            
            laps = session.laps
            
            fig = go.Figure()
            
            for driver in others:
                # Calculate gap
                # This is a simplified gap calculation. 
                # FastF1 doesn't have a direct "Gap to Leader" for every lap easily accessible without some processing.
                # We will use the accumulated lap times to calculate the gap at the end of each lap.
                
                d1_laps = laps.pick_drivers(ref_driver)
                d2_laps = laps.pick_drivers(driver)
                
                # Merge on LapNumber
                merged = pd.merge(d1_laps[['LapNumber', 'Time']], d2_laps[['LapNumber', 'Time']], on='LapNumber', suffixes=(f'_{ref_driver}', f'_{driver}'))
                
                # Calculate gap (Time delta)
                # Positive gap means Ref is ahead (Driver 2 time > Ref time)
                # Negative gap means Ref is behind
                merged['Gap'] = (merged[f'Time_{driver}'] - merged[f'Time_{ref_driver}']).dt.total_seconds()
                
                fig.add_trace(go.Scatter(
                    x=merged['LapNumber'], 
                    y=merged['Gap'], 
                    mode='lines+markers', 
                    name=f"Gap: {ref_driver} vs {driver}"
                ))
            
            fig.update_layout(
                title=f"Gap to {ref_driver} (Positive = {ref_driver} is Ahead)",
                xaxis_title="Lap Number",
                yaxis_title="Gap (s)",
                template="plotly_dark",
                height=500,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, width="stretch")
            
        except Exception as e:
            st.error(f"Error calculating gaps: {e}")

def render_position_chart(session, selected_drivers):
    """
    Render a position chart (bumphart) for all drivers or selected drivers.
    """
    with st.spinner("Generating position chart..."):
        try:
            # Get all laps
            laps = session.laps
            
            # Filter for selected drivers if any, otherwise show all (or top 10 for clarity)
            if selected_drivers:
                drivers_to_show = selected_drivers
            else:
                # Default to top 10 finishers if no drivers selected
                drivers_to_show = session.results['Abbreviation'].iloc[:10].tolist()
            
            # Filter laps
            laps_filtered = laps[laps['Driver'].isin(drivers_to_show)]
            
            # Create the plot
            fig = px.line(
                laps_filtered, 
                x='LapNumber', 
                y='Position', 
                color='Driver', 
                markers=True,
                title="Position Changes over Race",
                labels={'LapNumber': 'Lap', 'Position': 'Position'}
            )
            
            # Invert Y axis so P1 is at the top
            fig.update_yaxes(autorange="reversed")
            
            fig.update_layout(
                template="plotly_dark",
                height=500,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, width="stretch")
            
        except Exception as e:
            st.error(f"Error generating position chart: {e}")

def render_lap_data_table(session, selected_drivers):
    """
    Render a dataframe of lap data.
    """
    try:
        laps = session.laps
        
        if selected_drivers:
            laps = laps[laps['Driver'].isin(selected_drivers)]
            
        # Select relevant columns
        cols = ['Driver', 'LapNumber', 'LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time', 'Compound', 'TyreLife']
        
        # Format times for display
        display_laps = laps[cols].copy()
        
        # Convert Timedelta to string for better display
        for col in ['LapTime', 'Sector1Time', 'Sector2Time', 'Sector3Time']:
            display_laps[col] = display_laps[col].apply(lambda x: str(x).split('days')[-1].strip() if pd.notnull(x) else '')

        st.dataframe(display_laps, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error displaying lap data: {e}")
