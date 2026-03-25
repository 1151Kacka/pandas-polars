import pandas as pd
df = pd.read_csv("physics_solar_panel_lab_dataset.csv")
#1
print(df.head())    # Prvních 5 řádků
print(df.info())    # Datové typy a prázdné hodnoty
print(df.shape)     # Počet řádků a sloupců

#2 
df["lamp_distance_cm"] = df["lamp_distance_cm"].str.replace("cm", "", regex=False).str.strip()  # cm a mezery
for col in ["voltage_v", "current_a", "lamp_distance_cm", "temperature_c"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")   #datové typy
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")#datetime
df["panel_id"] = df["panel_id"].str.replace("SP_", "SP-", regex=False)#_na-
# weather
df["weather"] = df["weather"].str.strip().str.lower()
df["weather"] = df["weather"].str.replace("suny", "sunny")
df["weather"] = df["weather"].str.replace("indoor lamp", "indoor-lamp")
# room
df["room"] = df["room"].str.strip()
df["room"] = df["room"].str.replace("lab-1", "Lab-1")
# Duplicity
df = df.drop_duplicates()
# Záporné a nesmyslné hodnoty
df = df[df["power_w"] >= 0]
df = df[df["light_intensity_lux"] >= 0]
df = df[df["lamp_distance_cm"] >= 0]
df = df[df["angle_deg"].between(0, 90)]
# Chybějící hodnoty
df = df.dropna(subset=["voltage_v", "current_a", "power_w"])
print(f"\nDataset po čištění: {df.shape[0]} řádků, {df.shape[1]} sloupců")
print("\nUnikátní weather:", df["weather"].unique())
print("Unikátní room:   ", df["room"].unique())
print("Unikátní panel:  ", df["panel_id"].unique())

# 3
df["power_calc"] = (df["voltage_v"] * df["current_a"]).round(3)

diff = (df["power_calc"] - df["power_w"]).abs()
print(f"rozdílná hodnota: {diff.mean():.4f} W")

# 4

df["angle_group"] = (df["angle_deg"] // 10 * 10).astype(int)
vykon_uhel = df.groupby("angle_group")["power_w"].mean().round(3)
print("\nPrůměrný výkon podle úhlu (°):")
print(vykon_uhel)

# 5

korelace = df["light_intensity_lux"].corr(df["power_w"])
print(f"\nKorelace light_intensity_lux vs power_w: {korelace:.3f}")

print("\nPrůměrná intenzita světla podle prostředí:")
print(df.groupby("room")["light_intensity_lux"].mean().round(0).sort_values(ascending=False))

#6
vykon_room = df.groupby("room")["power_w"].mean().round(3).sort_values(ascending=False)
print("\nPrůměrný výkon podle lokace:")
print(vykon_room)

vykon_weather = df.groupby("weather")["power_w"].mean().round(3).sort_values(ascending=False)
print("\nPrůměrný výkon podle počasí:")
print(vykon_weather)

# 7 
df_bez_anomalii = df[df["power_w"] < 10]
nejlepsi = df_bez_anomalii.loc[df_bez_anomalii["power_w"].idxmax()]
print("\nNejlepší měření (bez anomálií):")
print(nejlepsi[["panel_id", "angle_deg", "room", "weather",
                "light_intensity_lux", "power_w"]])


# 8

Q1 = df["power_w"].quantile(0.25)
Q3 = df["power_w"].quantile(0.75)
IQR = Q3 - Q1
hranice = Q3 + 1.5 * IQR

anomalie = df[df["power_w"] > hranice]
print("\nAnomalní záznamy:")
print(anomalie[["panel_id", "room", "weather", "light_intensity_lux",
                "voltage_v", "current_a", "power_w", "notes"]].to_string())

# 9

kor_teplota = df["temperature_c"].corr(df["power_w"])
print(f"\nKorelace teplota vs výkon: {kor_teplota:.3f}")

# Int64 zvládne NaN hodnoty (na rozdíl od int)
df["temp_group"] = (df["temperature_c"] // 5 * 5).astype("Int64")
print("\nPrůměrný výkon podle teplotní skupiny (°C):")
print(df.groupby("temp_group")["power_w"].mean().round(3))

# Uložení 
df.drop(columns=["angle_group", "temp_group"], inplace=True)
df.to_csv("physics_solar_panel_cleaned.csv", index=False)
print("\n✓ Vyčištěný dataset uložen jako: physics_solar_panel_cleaned.csv")