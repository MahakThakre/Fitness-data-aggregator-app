# Fitness Tracker Data Aggregator

This Streamlit app aggregates and analyzes fitness tracker data from CSV and JSON files. It provides user statistics, daily top performers, and interactive visualizations.

---

## Sample Data Included

- Predefined **sample data** files are named:  
  - `sample_data.csv`  
  - `sample_data.json`  

These enable the app to run **without requiring user input**, providing default fitness data for immediate trial and analysis.

---

## Trial Data for Users

- For more extensive testing, a **100-row trial dataset** is provided as:  
  - `fitness_data.csv`  
  - `fitness_data.json`  

These files contain richer real-world style data suitable for robust testing.

---

## App Input Behavior

- By default, a **checkbox labeled "Use Sample Data"** is checked, so the app loads and analyzes the predefined `sample_data.csv` and `sample_data.json`.
- To use your own CSV or JSON files, **uncheck** this checkbox and upload your data files.
- The app will then perform cleaning, aggregation, and visualization on your uploaded files.

---

## Features

- Upload fitness data in CSV and/or JSON formats or use predefined sample data
- Data cleaning: date normalization, duplicate removal, missing value handling
- User statistics: total steps, total calories, weekly average steps
- Daily top user by steps
- Interactive charts (Plotly)
- Download results as JSON

---

## File Formats

### CSV

Required columns: `date`, `user_id`, `steps`, `calories`, `sleep_minutes`  
Various date formats are supported (e.g., `2025-09-01`, `01/09/2025`, `08-09-2025`).

### JSON

Array of objects, each with keys: `date`, `user_id`, `steps`, `calories`, `sleep_minutes`

---

## Usage

1. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```
2. **Run the app**:
    ```
    streamlit run fitness_tracker_app.py
    ```
3. **By default, sample data is loaded**; to analyze your own data, uncheck "Use Sample Data" checkbox and upload files.

---

## Output

- View per-user statistics and daily top users in the browser
- Download the computed summary as `fitness_results.json`

---

## Requirements

See [requirements.txt](requirements.txt)

---

## Sample Data Files

- Predefined small sample: `sample_data.csv`, `sample_data.json`  
- Trial 100-row dataset: `fitness_data.csv`, `fitness_data.json`

---
