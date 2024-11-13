#step 2

## This file concatenates all the formatted csvs together, divided by UF and
## put them in the INMET_TOTAL folder


import pandas as pd
import glob



UF = "SE_SP"
file_list_diaria = glob.glob(f"./INMET_*/arquivos_finais/temperatura_diaria/{UF}_Temperatura_diaria_*", recursive=True)
file_list_mensal = glob.glob(f"./INMET_*/arquivos_finais/temperatura_mensal/{UF}_Temperatura_mensal_*", recursive=True)

list_of_df_per_day = []
list_of_df_per_month = []

for file in file_list_diaria:
    df = pd.read_csv(file)
    list_of_df_per_day.append(df)

for file in file_list_mensal:
    df = pd.read_csv(file)
    list_of_df_per_month.append(df)

total_df_by_days = pd.concat(list_of_df_per_day)
total_df_by_month = pd.concat(list_of_df_per_month)
total_df_by_days = total_df_by_days.sort_values(by=["City","Period"])
total_df_by_month = total_df_by_month.sort_values(by=["City","Period"])


total_df_by_days.to_csv(f"./INMET_TOTAL/{UF}/{UF}_total_by_day_temperature.csv", index=False)
total_df_by_month.to_csv(f"./INMET_TOTAL/{UF}/{UF}_total_by_month_temperature.csv", index=False)