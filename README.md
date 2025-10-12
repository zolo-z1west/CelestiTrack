# Deep Orbit Trajectory Model (DOTM)

## Overview
Deep Orbit Trajectory Model (DOTM) is a machine learning system designed to predict satellite trajectories using real-time data collected from the Stellarium API. The project merges astronomy, data science, and AI to create accurate, dataset-driven predictions of orbital motion while generating clean, structured datasets suitable for further analysis or Kaggle publication.

Stellarium provides a detailed view of celestial bodies and their real-time positions. However, it is primarily a visualization and simulation tool, not a predictive or analytical one. DOTM bridges this gap by extracting numerical data from Stellarium’s Remote Control API, processing it into machine-learning-ready datasets, and using time-series deep learning models to predict future satellite positions.

---

## Objectives
- Collect real-time satellite positional data (RA/Dec, azimuth, altitude, timestamp) from Stellarium.  
- Convert and preprocess this data into suitable numerical formats for modeling.  
- Train AI/ML models capable of predicting future satellite positions based on historical data.  
- Visualize prediction performance and compare against actual or SGP4-propagated positions.  
- Package the processed datasets for Kaggle, ensuring reproducibility and community contribution.

---

## Features
- Automated Stellarium data collection pipeline  
- Time-series preprocessing and normalization tools  
- Reproducible dataset generation scripts  
- Baseline PyTorch models (LSTM/GRU) for trajectory prediction  
- Visualization utilities for predicted vs actual orbits  
- Kaggle-ready dataset export  

---

## Tech Stack
**Core Languages & Libraries**
- Python  
- Pandas, NumPy, Astropy, Matplotlib  
- PyTorch (for ML modeling)  
- SGp4 (for orbital propagation comparison)  
- OpenCV (for optional visual data integration)  

**Data Source**
- Stellarium Remote Control API (JSON output)

---

## System Architecture

### 1. Data Collection
Python script polls Stellarium API at fixed intervals to collect satellite parameters (RA, Dec, altitude, azimuth, timestamp).  

### 2. Data Preprocessing
- Converts celestial coordinates to 3D Cartesian vectors.  
- Normalizes and formats the data into sequential time windows.  

### 3. Model Training
- Uses LSTM/GRU networks to predict next-step orbits based on prior motion.  
- Evaluates error metrics (MSE, angular deviation).  

### 4. Evaluation and Visualization
- Plots predicted vs actual trajectories.  
- Allows comparison with classical physics models (SGP4).  

### 5. Dataset Packaging
- Exports final cleaned datasets for Kaggle upload and community use.  

---

## Directory Structure
```
Deep-Orbit-Trajectory-Model/
│
├── data/
│   ├── raw/                 # Raw Stellarium API data
│   ├── processed/           # Preprocessed and normalized datasets
│   └── kaggle/              # Final Kaggle-ready datasets
│
├── src/
│   ├── collector.py         # Stellarium data collection script
│   ├── preprocess.py        # Data cleaning and conversion
│   ├── model.py             # ML model definitions
│   ├── train.py             # Model training and evaluation
│   └── visualize.py         # Orbit and prediction visualization
│
├── notebooks/
│   └── baseline.ipynb       # Jupyter notebook demonstrating pipeline
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/zolo-z1west/Deep-Orbit-Trajectory-Model.git
cd Deep-Orbit-Trajectory-Model
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Stellarium Remote Control
- Enable the Remote Control plugin in Stellarium.  
- Ensure the API is running on port 8090 (default).  

### 5. Run data collection
```bash
python src/collector.py
```

### 6. Train the model
```bash
python src/train.py
```

### 7. Visualize results
```bash
python src/visualize.py
```

---

## Dataset Format
Each collected record includes:

| Column     | Description                      |
|------------|----------------------------------|
| timestamp  | UTC time of capture               |
| ra         | Right Ascension (degrees)         |
| dec        | Declination (degrees)             |
| az         | Azimuth (degrees)                 |
| alt        | Altitude (degrees)                |
| sat_id     | Satellite identifier              |
| x, y, z    | Converted Cartesian coordinates   |

---

## Future Extensions
- Hybrid physics-ML prediction using residual learning.  
- Integration with computer vision for image-based trajectory validation.  
- Real-time orbit visualization dashboard.  
- Public Kaggle dataset hosting and leaderboard.  

---

## License
This project is licensed under the MIT License.  

---


