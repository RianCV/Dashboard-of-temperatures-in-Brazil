#step 1

#this file deals with the gross files of precipitation in brazil, removing unnecessary columns and 
#adding a status column, showing if the temperature is regular, perfect or a danger for the region

import pandas as pd
import glob # to get all files from the same state

ano = "2023" #selecionar ano
uf = "CO_DF" #selecionar uf

base_file_name = f"./INMET_{ano}/INMET_{uf}*"
files = glob.glob(base_file_name)
cities_dataframes = []
cities_dataframes_by_month = []

for file in files:
    df = pd.read_csv(file, encoding="latin1", nrows=5, delimiter=';') ## The data came formatted with a mini
    city_name = df.iloc[1,1]                                          ##top table, which contains the name of the city

    df = pd.read_csv(file, encoding="latin1", skiprows=8, delimiter=';')
    df = df.iloc[:, [0,7]] #Taking only the date and temperature columns
    df.iloc[:,1] = df.iloc[:,1].str.replace(',','.').astype(float) #change ',' for '.' and transform string to float
    df = df.rename(columns={"TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)":"Temperature"})

    grouped = df.groupby("Data")["Temperature"].mean().reset_index() #grouping the average temperatures per day
    grouped["Temperature"] = grouped["Temperature"].astype(float).round()

    mean_temperature = grouped["Temperature"].mean().round()                 #putting the average temperatures
    grouped["Temperature"] = grouped["Temperature"].fillna(mean_temperature) #on the zeroed lines


    grouped.insert(0, "City", city_name, True)
    grouped.insert(3,"Status", 0, True)

    #adding values to the status column depending on the temperature, with values Regular, Perfect, or danger
    grouped["Status"] = grouped.apply(lambda row: 
                                      "Regular" if (row["Temperature"] >= 10.0 and row["Temperature"] < 24.0) 
                                      else("Perfect" if (row["Temperature"] >= 24.0 and row["Temperature"] <= 30.0) 
                                      else "danger"), axis=1)
    
    grouped.rename(columns={"Data": "Period"}, inplace=True)

    cities_dataframes.append(grouped)


    #Transforming data from daily to monthly
    new_grouped = grouped.copy(deep=True)
    new_grouped["Period"] = pd.to_datetime(new_grouped["Period"])
    new_grouped["Period"] = new_grouped["Period"].dt.to_period("M")
    grouped_by_month = new_grouped.groupby("Period")["Temperature"].mean().round().reset_index()
    grouped_by_month["Status"] = grouped_by_month.apply(lambda row: 
                                                        "Regular" if (row["Temperature"] >= 10.0 and row["Temperature"] < 24.0) 
                                                        else("Perfect" if (row["Temperature"] >= 24.0 and row["Temperature"] <= 30.0) 
                                                        else "danger"), axis=1)
    grouped_by_month.insert(0, "City", city_name, True)
    cities_dataframes_by_month.append(grouped_by_month)

#saving the formatted files to the 'final files' folders, for daily and monthly files
combined_df = pd.concat(cities_dataframes)
combined_df.to_csv(f"./INMET_{ano}/arquivos_finais/temperatura_diaria/{uf}_Temperatura_diaria_{ano}.csv", index= False)

combined_df_by_month = pd.concat(cities_dataframes_by_month)
combined_df_by_month.to_csv(f"./INMET_{ano}/arquivos_finais/temperatura_mensal/{uf}_Temperatura_mensal_{ano}.csv", index= False)