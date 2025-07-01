# GPS Spoofing Simulation and Detection using Python, RF Analysis & ML

This project presents a comprehensive study and implementation of GPS spoofing attacks and their detection using a combination of signal simulation, RF link budget analysis, and machine learning techniques.

## 📌 Overview

GPS spoofing is the act of deceiving a GPS receiver by broadcasting counterfeit GPS signals. This project simulates the spoofing process and evaluates both the feasibility of attacks and the effectiveness of real-time detection models.

---

## 🔧 Components

### 1. GPS Signal Simulation
- Simulates satellite signals in Earth-Centered Earth-Fixed (ECEF) coordinates.
- Implements trilateration to estimate receiver position.
- Adds Gaussian noise to emulate real-world conditions.
- Visualizes true vs. estimated position accuracy.

### 2. RF Link Budget Analysis
- Calculates required spoofing power using Free Space Path Loss (FSPL) and Carrier-to-Noise Ratio (C/N₀).
- Determines feasibility of spoofing from various distances (up to 5 km).
- Analyzes signal dominance over genuine satellite transmissions.

### 3. Spoofing Simulation on a Mobile Host
- Simulates a moving GPS receiver (e.g., drone/vehicle) being spoofed mid-path.
- Demonstrates deviation from the original trajectory post-attack.
- Visualizes true path vs. spoofed trajectory.

### 4. Machine Learning-Based Spoofing Detection
- Extracts features like displacement, speed, and acceleration from GPS traces.
- Injects synthetic spoofing points to simulate anomalies.
- Trains a supervised ML model to classify spoofed vs. normal data points.
- Achieves high precision with real-time detection capability.

---

## 📈 Results

- **Position Estimation Error**: ~7–13 meters under noise.
- **Spoofing Power Requirement**: ~3.2 kW at 5 km range.
- **Detection Model Performance**:
  - Precision: 100%
  - F1-Score: 61.5%
  - Recall: 44.4%

---

## 📁 File Structure

