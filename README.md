# Data manipulation with pandas and building a dashboard with Dash

Construction of an interactive dashboard on the daily and monthly rainfall of Brazilian cities between 2019 and 2023.

## Raw data from INMET (National Meteorological Mnstitute):
    COLOCAR IMAGEM

1. In the app.py file, we select only the date and temperature columns, add the average for missing values, add a status column, which will show whether or not the temperature in a given period is harmful to the soil, and save the new data in another folder.

2. In agregate.py we do some basic file manipulation to concatenate different dates into a single file

## Final file after manipulation:

    COLOCAR IMAGEM DE COMO FICA O FILE NO FINAL (dizer que eh diario)

## Dashboard

The dashboard.py file creates the interactive dashboard

To execute:
    python dashboard.py