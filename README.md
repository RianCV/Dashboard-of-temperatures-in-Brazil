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

Execute dashboard.py to see the dashboard.

<img width="1055" alt="image" src="https://github.com/user-attachments/assets/3690ad7a-7ce4-4656-b9ce-7c86be6eeebf" />

<img width="1055" alt="image" src="https://github.com/user-attachments/assets/c8927e9a-dfc4-4753-a92a-b1d675808f0b" />

<img width="1055" alt="image" src="https://github.com/user-attachments/assets/d79f03e1-2e4a-41c6-add1-48b653c8bc0c" />
