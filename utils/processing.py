import pandas as pd
import numpy as np

def calculate_overtakes(laps):
    """
    Calculate overtakes based on position changes.
    Returns a DataFrame of overtakes.
    """
    # Ensure laps are sorted by lap number
    laps = laps.sort_values(by=['Driver', 'LapNumber'])
    
    # Calculate position difference
    laps['PositionChange'] = laps.groupby('Driver')['Position'].diff()
    
    # Identify overtakes (negative change means improved position, e.g., 5 -> 4 is -1)
    overtakes = laps[laps['PositionChange'] < 0]
    
    return overtakes

def calculate_gap(laps, driver1, driver2):
    """
    Calculate the gap between two drivers over the race.
    Returns a DataFrame with LapNumber and Gap.
    """
    d1_laps = laps.pick_drivers(driver1)
    d2_laps = laps.pick_drivers(driver2)
    
    # Merge on LapNumber
    merged = pd.merge(d1_laps[['LapNumber', 'Time']], d2_laps[['LapNumber', 'Time']], on='LapNumber', suffixes=(f'_{driver1}', f'_{driver2}'))
    
    # Calculate gap (Time delta)
    merged['Gap'] = (merged[f'Time_{driver1}'] - merged[f'Time_{driver2}']).dt.total_seconds()
    
    return merged[['LapNumber', 'Gap']]
