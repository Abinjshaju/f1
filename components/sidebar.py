import streamlit as st
from utils.data_loader import load_session

def render_sidebar():
    """
    Render the sidebar controls and return the selected parameters and loaded session.
    """
    st.sidebar.title("F1 Analytics 🏎️")
    st.sidebar.header("Session Selection")

    # Year Selector
    year = st.sidebar.selectbox("Year", [2024, 2023, 2022, 2021], index=0)

    # Grand Prix Selector
    circuits = ["Bahrain", "Saudi Arabia", "Australia", "Japan", "China", "Miami", "Emilia Romagna", "Monaco", "Canada", "Spain", "Austria", "Great Britain", "Hungary", "Belgium", "Netherlands", "Italy", "Azerbaijan", "Singapore", "USA", "Mexico", "Brazil", "Las Vegas", "Qatar", "Abu Dhabi"]
    gp = st.sidebar.selectbox("Grand Prix", circuits, index=7) # Default to Monaco

    # Session Type Selector
    session_type = st.sidebar.selectbox("Session", ["FP1", "FP2", "FP3", "Qualifying", "Race", "Sprint"], index=4)

    # Load Data Button
    session = None
    if st.sidebar.button("Load Session Data", type="primary"):
        with st.spinner("Loading session data..."):
            try:
                session = load_session(year, gp, session_type)
                if session:
                    st.session_state['session'] = session
                    st.success(f"Loaded {year} {gp} {session_type}")
                else:
                    st.error("Failed to load session.")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Retrieve session from state if available
    if 'session' in st.session_state:
        session = st.session_state['session']
        
        st.sidebar.markdown("---")
        st.sidebar.header("Filter Controls")
        
        # Driver Selector
        drivers = sorted(session.results['Abbreviation'].unique())
        
        all_drivers = st.sidebar.checkbox("Select All Drivers")
        if all_drivers:
            selected_drivers = drivers
            # Show disabled multiselect to indicate all are selected
            st.sidebar.multiselect("Select Drivers", drivers, default=drivers, disabled=True, key="drivers_multiselect_all")
        else:
            selected_drivers = st.sidebar.multiselect("Select Drivers", drivers, default=drivers[:2], key="drivers_multiselect")
        
        # Lap Selector (Range)
        total_laps = int(session.laps['LapNumber'].max())
        selected_laps = st.sidebar.slider("Select Laps", 1, total_laps, (1, total_laps))
        
        return {
            "year": year,
            "gp": gp,
            "session_type": session_type,
            "session": session,
            "selected_drivers": selected_drivers,
            "selected_laps": selected_laps
        }
    
    return None
