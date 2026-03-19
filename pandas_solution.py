import pandas as pd
df = pd.read_csv("physics_solar_panel_lab_dataset.csv")
#1
print(df.head())    # Prvních 5 řádků
print(df.info())    # Datové typy a prázdné hodnoty
print(df.shape)     # Počet řádků a sloupců

#2 
df["voltage_v"] = pd.to_numeric(df["voltage_v"], errors="coerce")
df["current_a"] = pd.to_numeric(df["current_a"], errors="coerce")
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
#Chybějící hodnoty:
df.isna()
df.fillna(0)
df.drop_duplicates()