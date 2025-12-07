# F1 Race Analytics Dashboard

## Overview

The **F1 Race Analytics Dashboard** is a high-fidelity, interactive telemetry analysis tool designed for Formula 1 enthusiasts and data analysts. Built on top of the `FastF1` library, this application leverages public F1 API data to provide granular insights into race performance, strategy, and vehicle dynamics.

The system employs a split-screen architecture, juxtaposing spatial circuit analysis with time-series telemetry data, enabling users to correlate track position with vehicle performance metrics in real-time.

## Architecture

The application follows a modular component-based architecture using **Streamlit** as the frontend framework.

### Tech Stack

*   **Core Engine**: Python 3.10+
*   **Data Ingestion**: `FastF1` (with persistent caching)
*   **Data Processing**: `Pandas`, `NumPy`
*   **Visualization**: `Plotly Express`, `Plotly Graph Objects`
*   **Frontend**: `Streamlit`
*   **Package Management**: `uv`

### Directory Structure

```
f1/
├── main.py                 # Application entry point and layout orchestration
├── components/             # UI Components
│   ├── sidebar.py          # Session and driver selection logic
│   ├── track_map.py        # Spatial visualization (Track Map, Corners)
│   ├── telemetry.py        # Time-series telemetry (Speed, RPM, Throttle/Brake)
│   ├── strategy.py         # Strategy analysis (Tyre Stints, Pace Distribution)
│   └── lap_analysis.py     # Race progression (Position Charts, Gap Analysis)
├── utils/                  # Core Utilities
│   ├── data_loader.py      # Data fetching and caching abstraction
│   ├── processing.py       # Analytical computations (Overtakes, Gaps)
│   └── styling.py          # Custom CSS injection
└── cache/                  # Local filesystem cache for FastF1 API responses
```

## Key Features

### 1. Spatial Telemetry Analysis
*   **Interactive Track Map**: 2D projection of circuit coordinates.
*   **Data Layering**: Dynamic coloring of the racing line based on telemetry channels (Speed, Gear, Brake).
*   **Circuit Annotation**: Automated labeling of corner numbers derived from circuit metadata.

### 2. Advanced Telemetry Traces
*   **Multi-Channel Plotting**: Synchronized subplots for Speed (km/h), Engine RPM, Gear, Throttle (%), and Brake pressure (binary/pressure).
*   **Fastest Lap Comparison**: Automatically fetches and aligns the fastest lap for selected drivers for direct comparison.

### 3. Strategy & Race Dynamics
*   **Tyre Stint History**: Gantt-style visualization of tyre compound usage and stint lengths.
*   **Pace Analysis**: Box plot distributions of lap times to evaluate driver consistency and degradation.
*   **Gap Analysis**: Time-delta visualization relative to a reference driver to identify undercuts/overcuts.
*   **Position Evolution**: "Bumphart" visualization tracking position changes across all laps.

## Installation & Usage

### Prerequisites

*   Python 3.10 or higher
*   `uv` (recommended) or `pip`

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Abinjshaju/f1.git
    cd f1
    ```

2.  **Install dependencies:**
    ```bash
    uv pip install -r requirements.txt
    # OR
    pip install fastf1 streamlit plotly pandas
    ```

3.  **Run the application:**
    ```bash
    uv run streamlit run main.py
    ```

## Caching Strategy

To mitigate the latency of the F1 API, the application implements a persistent filesystem cache in the `./cache` directory. Initial session loads may take 30-60 seconds, while subsequent loads are near-instantaneous.

## License

[MIT License](LICENSE)
