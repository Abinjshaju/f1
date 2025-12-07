import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Main container styling */
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #161b22;
        }
        
        /* Custom headers */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
        }
        
        /* Card-like containers for metrics */
        .metric-card {
            background-color: #1f2937;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #374151;
            margin-bottom: 1rem;
        }
        
        /* Plotly chart background */
        .js-plotly-plot .plotly .main-svg {
            background-color: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)
