import polars as pl
df = pl.read_csv(
    "physics_solar_panel_lab_dataset.csv",
    separator=",",
    decimal_comma=False,
    infer_schema_length=0,   # vše text
    ignore_errors=True
)

# 1

print("\nPrvních 5 řádků:")
print(df.head())
 
print(f"\nPočet řádků:   {df.shape[0]}")
print(f"Počet sloupců: {df.shape[1]}")
 
print("\nDatové typy (schema):")
print(df.schema)
 
# 2

df = df.with_columns(
    pl.col("lamp_distance_cm").str.replace("cm", "").str.strip_chars() #cm X
)
 
#převedení
for col in ["lamp_distance_cm", "voltage_v", "current_a", "temperature_c", "power_w", "light_intensity_lux", "angle_deg"]:
    df = df.with_columns(
        pl.col(col).cast(pl.Float64, strict=False)
    )
df = df.with_columns(
    pl.col("timestamp").str.strptime(pl.Datetime, "%Y-%m-%d %H:%M:%S", strict=False)
)
# sjednocení
df = df.with_columns(
    pl.col("weather").str.strip_chars().str.to_lowercase(),
    pl.col("room").str.strip_chars(),
    pl.col("panel_id").str.strip_chars()
)
# překlepy
df = df.with_columns(
    pl.col("weather").str.replace("suny", "sunny")
                     .str.replace("indoor lamp", "indoor-lamp"),
    pl.col("room").str.replace("lab-1", "Lab-1"),
    pl.col("panel_id").str.replace("SP_", "SP-")
)
# Duplicity 
pocet_pred = df.shape[0]
df = df.unique()
print(f"\nOdstraněno duplicit: {pocet_pred - df.shape[0]}")
# nesmysly
df = df.filter(
    (pl.col("power_w") >= 0) &
    (pl.col("light_intensity_lux") >= 0) &
    (pl.col("lamp_distance_cm") >= 0) &
    (pl.col("angle_deg") >= 0) &
    (pl.col("angle_deg") <= 90)
)
# Chybí
print("\nChybějící hodnoty (null) po čištění:")
print(df.null_count())
# Odstranění
df = df.drop_nulls(subset=["voltage_v", "current_a", "power_w"])
 
print(f"\nDataset po čištění: {df.shape[0]} řádků")
print("\nUnikátní weather:", df["weather"].unique().to_list())
print("Unikátní room:   ", df["room"].unique().to_list())
print("Unikátní panel:  ", df["panel_id"].unique().to_list())
 
# 3
# vzorec
df = df.with_columns(
    (pl.col("voltage_v") * pl.col("current_a")).alias("power_calc")
)
# Porovnání 
df = df.with_columns(
    (pl.col("power_calc") - pl.col("power_w")).abs().alias("power_diff")
)
 
prumer_diff = df["power_diff"].mean()
max_diff = df["power_diff"].max()
print(f"\nPrůměrný absolutní rozdíl power_calc vs power_w: {prumer_diff:.4f} W")
print(f"Maximální rozdíl: {max_diff:.4f} W")
 
# 4 vliv
vykon_uhel = (
    df.group_by("angle_deg")
    .agg(pl.col("power_w").mean().alias("prumerny_vykon"))
    .sort("angle_deg")
)
print("\nPrůměrný výkon podle úhlu (°):")
print(vykon_uhel)
 
# 5 vliv
korelace = df.select(pl.corr("light_intensity_lux", "power_w"))
print(f"\nKorelace light_intensity_lux vs power_w:")
print(korelace) 
# 6
vykon_weather = (
    df.group_by("weather")
    .agg(pl.col("power_w").mean().alias("prumerny_vykon"))
    .sort("prumerny_vykon", descending=True)
)
print("\nPrůměrný výkon podle počasí:")
print(vykon_weather)
 
vykon_room = (
    df.group_by("room")
    .agg(pl.col("power_w").mean().alias("prumerny_vykon"))
    .sort("prumerny_vykon", descending=True)
)
print("\nPrůměrný výkon podle lokace:")
print(vykon_room)
 
# 7
top5 = (
    df.sort("power_w", descending=True)
    .select(["panel_id", "angle_deg", "room", "weather", "power_w"])
    .head(5)
)
print("\nTop 5 měření s nejvyšším výkonem:")
print(top5)

# 8
 
anomalie = df.filter(pl.col("power_w") > 10)
print(f"\nPočet záznamů s power_w > 10 W: {anomalie.shape[0]}")
print(anomalie.select(["panel_id", "room", "weather",
                        "light_intensity_lux", "voltage_v",
                        "current_a", "power_w", "notes"]))
 
# 9 
# Korelace teplota vs výkon
kor_teplota = df.select(pl.corr("temperature_c", "power_w"))
print(f"\nKorelace teplota vs výkon:")
print(kor_teplota)
 
# Průměrný výkon pro různá teplotní pásma (filtr + group_by)
# Rozdělíme na: studené (<15°C), střední (15–25°C), teplé (>25°C)
studene = df.filter(pl.col("temperature_c") < 15)["power_w"].mean()
stredni = df.filter(
    (pl.col("temperature_c") >= 15) & (pl.col("temperature_c") <= 25)
)["power_w"].mean()
tople = df.filter(pl.col("temperature_c") > 25)["power_w"].mean()
 
print(f"\nPrůměrný výkon:")
print(f"  Studené podmínky (<15 °C):   {studene:.3f} W")
print(f"  Střední podmínky (15–25 °C): {stredni:.3f} W")
print(f"  Teplé podmínky (>25 °C):     {tople:.3f} W")