import pandas as pd
import numpy as np

# ==========================================
# 1. Carga y limpieza de datos (Temperatura)
# ==========================================
# URLs directas al formato Raw de GitHub
url_temp = "https://raw.githubusercontent.com/Mariana541-M/Taller-5B---Doing-Economics/main/Raw%20data/Anomal%C3%ADa%20de%20temperatura.csv"

df_temp = pd.read_csv(url_temp, skiprows=1)
df_temp = df_temp.apply(pd.to_numeric, errors='coerce')

# ==========================================
# PARTE 1.2: Variación de la temperatura
# ==========================================
df_51_80 = df_temp[(df_temp['Year'] >= 1951) & (df_temp['Year'] <= 1980)]
df_81_10 = df_temp[(df_temp['Year'] >= 1981) & (df_temp['Year'] <= 2010)]

bins = np.arange(-0.5, 1.55, 0.05)
freq_51_80 = pd.cut(df_51_80['J-D'].dropna(), bins=bins).value_counts().sort_index()
freq_81_10 = pd.cut(df_81_10['J-D'].dropna(), bins=bins).value_counts().sort_index()

print("--- Pregunta 1.2.1: Frecuencias ---")
print(freq_51_80)
print(freq_81_10)

q3_51_80 = np.quantile(df_51_80['J-D'].dropna(), 0.3)
q7_51_80 = np.quantile(df_51_80['J-D'].dropna(), 0.7)

total_81_10 = len(df_81_10['J-D'].dropna())
calientes_81_10 = len(df_81_10[df_81_10['J-D'] > q7_51_80])
porcentaje = (calientes_81_10 / total_81_10) * 100

print("\n--- Preguntas 1.2.3 y 1.2.4 ---")
print(f"Decil 3 (1951-1980): {q3_51_80}")
print(f"Decil 7 (umbral 'caliente'): {q7_51_80}")
print(f"Anomalías 'calientes' (1981-2010): {porcentaje:.2f}%")

df_21_50 = df_temp[(df_temp['Year'] >= 1921) & (df_temp['Year'] <= 1950)]
estaciones = ['DJF', 'MAM', 'JJA', 'SON']

print("\n--- Pregunta 1.2.5: Varianza Estacional ---")
print("1921-1950:\n", df_21_50[estaciones].agg(['mean', 'var']))
print("\n1951-1980:\n", df_51_80[estaciones].agg(['mean', 'var']))
print("\n1981-2010:\n", df_81_10[estaciones].agg(['mean', 'var']))

# ==========================================
# PARTE 1.3: CO2 y su relación con la temperatura
# ==========================================
# URL directa al formato Raw de GitHub
url_co2 = "https://raw.githubusercontent.com/Mariana541-M/Taller-5B---Doing-Economics/main/Raw%20data/1_CO2-data.csv"

# Carga con separador de punto y coma y reconocimiento de decimales
df_co2 = pd.read_csv(url_co2, sep=';', decimal=',')

# Filtrar CO2 para el mes de Enero (Month == 1)
df_co2_jan = df_co2.loc[df_co2['Month'] == 1].copy()

# Unir usando la llave 'Year' (mayúscula en ambas bases)
df_merged = pd.merge(df_temp[['Year', 'Jan']], df_co2_jan[['Year', 'Trend']], on='Year')

# Forzar tipo numérico para evitar errores de cálculo
df_merged['Jan'] = df_merged['Jan'].astype(float)
df_merged['Trend'] = df_merged['Trend'].astype(float)

# Coeficiente de correlación
correlacion = df_merged['Jan'].corr(df_merged['Trend'])

print("\n--- Pregunta 1.3.4 ---")
print(f"Correlación de Pearson (Enero vs Tendencia CO2): {correlacion:.4f}")