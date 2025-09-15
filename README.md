# Fitness Tracker Data Aggregator

This Streamlit app aggregates and analyzes fitness tracker data from CSV and JSON files. It provides user statistics, daily top performers, and interactive visualizations.

---

## Features

- Upload fitness data in CSV and JSON formats
- Data cleaning: date normalization, duplicate removal, missing value handling
- User statistics: total steps, total calories, weekly average steps
- Daily top user by steps
- Interactive charts (Plotly)
- Download results as JSON

---

## App Working

1. **Upload Data**: Upload one or both of CSV and JSON fitness data files (with required structure).
2. **Automatic Cleaning**: The app normalizes date formats, removes duplicate (user+date) entries, and fills in missing values such as calories per-user average.
3. **Statistics Generation**: Computes total steps and calories for each user and their weekly average steps. Also finds the daily top user by step count.
4. **Interactive Reporting**: View statistics and daily leaders on screen. Explore trends and patterns through interactive Plotly charts.
5. **Download Output**: Download the cleaned and aggregated results as a compliant JSON file instantly.

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
3. **Upload your data files** (or use the pre-provided sample datasets)

---

## Output

- View per-user statistics and daily top users in the browser
- Download the computed summary as `fitness_results.json`

---

## Requirements

See [requirements.txt](requirements.txt)

---

## Sample Data

- [fitness_data.csv](fitness_data.csv)
- [fitness_data.json](fitness_data.json)

---
