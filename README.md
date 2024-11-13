# Data manipulation with pandas and building a dashboard using Dash

Construction of an interactive dashboard on the daily and monthly rainfall of Brazilian cities between 2019 and 2023.

## Raw data from INMET (National Meteorological Mnstitute):

<img width="1251" alt="inmet_bruto" src="https://github.com/user-attachments/assets/b9f275b9-0c31-4d79-89d3-26a8ce4cc6b5">

1. In the app.py file, we select only the date and temperature columns, add the average for missing values, add a status column, which will show whether or not the temperature in a given period is harmful to the soil, and save the new data in another folder.

2. In agregate.py we do some basic file manipulation to concatenate different dates into a single file.

## Final file example after manipulation:

<img width="369" alt="arquivo_final_diario" src="https://github.com/user-attachments/assets/4ccaf8a0-2227-41d4-8f2a-8b11acf3e901">

## Dashboard

The dashboard.py file creates the interactive dashboard.

To execute:
    python dashboard.py
