import fastf1
import pandas as pd
import os

# Enable caching
CACHE_DIR = 'cache'
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

fastf1.Cache.enable_cache(CACHE_DIR)

def load_session(year, gp, session_type):
    """
    Load a session from FastF1.
    """
    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load()
        return session
    except Exception as e:
        print(f"Error loading session: {e}")
        return None

def load_laps(session):
    """
    Load laps from a session.
    """
    return session.laps

def load_telemetry(session, driver_number=None):
    """
    Load telemetry for a session or specific driver.
    """
    if driver_number:
        return session.laps.pick_drivers(driver_number).get_telemetry()
    return session.laps.get_telemetry()
