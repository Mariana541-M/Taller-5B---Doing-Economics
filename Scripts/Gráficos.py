import pandas as pd
import matplotlib as npl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pingouin as pg
from lets_plot import *

LetsPlot.setup_html(no_js=True)
#Parte 1 
plt.style.use(
    "https://raw.githubusercontent.com/aeturrell/core_python/main/plot_style.txt"
)  
df = pd.read_csv(
    "https://data.giss.nasa.gov/gistemp/tabledata_v4/NH.Ts+dSST.csv",
    skiprows=1,
    na_values="***",
)
df.head()
df.info()
#Gráfico lineal de temperatura y tiempo
#Gráfico lineal de anomalías para un mes en específico

df = df.set_index("Year")
print(df.head())
df.tail()
print(df.tail())
month = "Feb"
fig, ax = plt.subplots()
ax.axhline(0, color="blue")
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(
    f"Average temperature anomaly in {month} \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");
import os
carpeta_destino = r"C:\Users\Mariana\Desktop\Taller 5B - Doing Economics\Graficos_Taller5B"
os.makedirs(carpeta_destino, exist_ok=True)

fig.savefig(os.path.join(carpeta_destino, f"grafico_{month}.png"), dpi=300, bbox_inches="tight")
#Gráfico lineal de anomalías de temperatura anuales 

month = "J-D"
fig, ax = plt.subplots()
ax.axhline(0, color="green")
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(
    f"Average temperature anomaly in {month} \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");
fig.savefig(os.path.join(carpeta_destino, f"grafico_{month}.png"), dpi=300, bbox_inches="tight")
#Gráfico lineal de anomalías de temperatura por estaciones

estaciones=["DJF","MAM","JJA","SON"]
fig, ax = plt.subplots()
ax.axhline(0, color="black")
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[estaciones].plot(ax=ax)
ax.set_title(
    f"Average temperature anomaly by season \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");
fig.savefig(os.path.join(carpeta_destino, f"grafico_{estaciones}.png"), dpi=300, bbox_inches="tight")

#Creación de tablas de frecuencia 

df["Period"] = pd.cut(
    df.index,
    bins=[1921, 1950, 1980, 2010],
    labels=["1921—1950", "1951—1980", "1981—2010"],
    ordered=True,
)
list_of_months = ["Jun", "Jul", "Aug"]

fig, axes = plt.subplots(ncols=3, figsize=(9, 4), sharex=True, sharey=True)
for ax, period in zip(axes, df["Period"].dropna().unique()):
    df.loc[df["Period"] == period, list_of_months].stack().hist(ax=ax)
    ax.set_title(period)
plt.suptitle("Histogram of temperature anomalies")
axes[1].set_xlabel("Summer temperature distribution")
plt.tight_layout();
df[list_of_months].stack().head()
fig.savefig(os.path.join(carpeta_destino, "histograma_anomalias_verano.png"), dpi=300, bbox_inches="tight")

#Percentiles y cuantiles

temp_all_months = df.loc[(df.index >= 1951) & (df.index <= 1980), "Jan":"Dec"]
temp_all_months = (
    temp_all_months.stack()
    .reset_index()
    .rename(columns={"level_1": "month", 0: "values"})
)
# Take a look at this data:
temp_all_months
quantiles = [0.3, 0.7]
list_of_percentiles = np.quantile(temp_all_months["values"], q=quantiles)

print(f"The cold threshold of {quantiles[0]*100}% is {list_of_percentiles[0]}")
print(f"The hot threshold of {quantiles[1]*100}% is {list_of_percentiles[1]}")

#Proporción de anomalías en un cuantil

temp_all_months = df.loc[(df.index >= 1981) & (df.index <= 2010), "Jan":"Dec"]
temp_all_months = (
    temp_all_months.stack()
    .reset_index()
    .rename(columns={"level_1": "month", 0: "values"})
)
temp_all_months.head()
entries_less_than_q30 = temp_all_months["values"] < list_of_percentiles[0]
proportion_under_q30 = entries_less_than_q30.mean()
print(
    f"The proportion under {list_of_percentiles[0]} is {proportion_under_q30*100:.2f}%"
)
proportion_over_q70 = (temp_all_months["values"] > list_of_percentiles[1]).mean()
print(f"The proportion over {list_of_percentiles[1]} is {proportion_over_q70*100:.2f}%")

#Cálculo y comprensión de la media y la varianza

temp_all_months = (
    df.loc[:, "DJF":"SON"]
    .stack()
    .reset_index()
    .rename(columns={"level_1": "Season", 0: "Values"})
)
temp_all_months["Period"] = pd.cut(
    temp_all_months["Year"],
    bins=[1921, 1950, 1980, 2010],
    labels=["1921—1950", "1951—1980", "1981—2010"],
    ordered=True,
)
temp_all_months.iloc[-135:-125]

# Varianza 
grp_mean_var = temp_all_months.groupby(["Season", "Period"])["Values"].agg(
    [np.mean, np.var]
)
grp_mean_var

#Anomalía media anual de la temperatura en el hemisferio norte, por estación del año

min_year = 1880
p=(
    ggplot(temp_all_months, aes(x="Year", y="Values", color="Season"))
    + geom_abline(slope=0, color="black", size=1)
    + geom_line(size=1)
    + labs(
        title=f"Average annual temperature anomaly in \n in the northern hemisphere ({min_year}—{temp_all_months['Year'].max()})",
        y="Annual temperature anomalies",
    )
    + scale_x_continuous(format="d")
    + geom_text(
        x=min_year, y=0.1, label="1951—1980 average", hjust="left", color="black"
    )
)
carpeta_destino = r"C:\Users\Mariana\Desktop\Taller 5B - Doing Economics\Graficos_Taller5B"
import os
import webbrowser
ruta = ggsave(p, "temp_anomaly.png", path=carpeta_destino)

#Importar archivo
df_co2 = pd.read_csv(
    r"C:\Users\Mariana\Desktop\Taller 5B - Doing Economics\Raw Data\1_CO2-data.csv",
    sep=";",
)
df_co2.head()
df_co2_june = df_co2.loc[df_co2["Month"] == 6]
df_co2_june.head()
df_temp_co2 = pd.merge(df_co2_june, df, on="Year")
df_temp_co2[["Year", "Jun", "Trend"]].head()

#Diagrama de dispersión 

df_temp_co2["Jun"] = df_temp_co2["Jun"].astype(str).str.replace(",", ".").astype(float)
df_temp_co2["Trend"] = df_temp_co2["Trend"].astype(str).str.replace(",", ".").astype(float)

p=(
    ggplot(df_temp_co2, aes(x="Jun", y="Trend"))
    + geom_point(color="pink", size=3)
    + labs(
        title="Scatterplot of temperature anomalies vs carbon dioxide emissions",
        y="Carbon dioxide levels (trend, mole fraction)",
        x="Temperature anomaly (degrees Celsius)",
    )
)
from lets_plot import *
LetsPlot.setup_html()

p = (
    ggplot(df_temp_co2, aes(x="Jun", y="Trend"))
    + geom_point(color="blue", size=3)
    + labs(
        title="Scatterplot of temperature anomalies vs carbon dioxide emissions",
        x="Temperature anomaly (degrees Celsius)",
        y="Carbon dioxide levels (trend, mole fraction)"
    )
)

import os
carpeta_destino = r"C:\Users\Mariana\Desktop\Taller 5B - Doing Economics\Graficos_Taller5B"
os.makedirs(carpeta_destino, exist_ok=True)

ggsave(p, filename="grafico_co2.png", path=carpeta_destino)

#Coeficiente de correlación
correlacion_june = df_temp_co2[["Jun", "Trend"]].corr(method="pearson")
print(correlacion_june)

#Gráfico anomalías temperatura Junio

g=(
    ggplot(df_temp_co2, aes(x="Year", y="Jun"))
    + geom_line(size=1)
    + labs(
        title="June temperature anomalies",
    )
    + scale_x_continuous(format="d")
)
carpeta_destino = r"C:\Users\Mariana\Desktop\Taller 5B - Doing Economics\Graficos_Taller5B"
os.makedirs(carpeta_destino, exist_ok=True)

ggsave(g, filename="Anomalias_junio.png", path=carpeta_destino)

#Anomalías de temperatura y emisiones de dióxido de carbono en junio.

base_plot = ggplot(df_temp_co2) + scale_x_continuous(format="d")
plot_p = (
    base_plot
    + geom_line(aes(x="Year", y="Jun"), size=1)
    + labs(title="June temperature anomalies")
)
plot_q = (
    base_plot
    + geom_line(aes(x="Year", y="Trend"), size=1)
    + labs(title="Carbon dioxide emissions")
)
x=gggrid([plot_p, plot_q], ncol=2)
ggsave(x, filename="Anomalias_Emisiones.png", path=carpeta_destino)

#Anomalías de temperatura y emisiones de dióxido de carbono en Enero

base_plot = ggplot(df_temp_co2) + scale_x_continuous(format="d")
plot_p = (
    base_plot
    + geom_line(aes(x="Year", y="Jan"), size=1)
    + labs(title="Jan temperature anomalies")
)
plot_q = (
    base_plot
    + geom_line(aes(x="Year", y="Trend"), size=1)
    + labs(title="Carbon dioxide emissions")
)
y=gggrid([plot_p, plot_q], ncol=2)
ggsave(y, filename="Anomalias_Emisiones_Enero.png", path=carpeta_destino)

#Coeficiente correlación Enero
correlacion_jan = df_temp_co2[["Jan", "Trend"]].corr(method="pearson")
print(correlacion_jan)

#Anomalías de temperatura y emisiones de dióxido de carbono en Diciembre

base_plot = ggplot(df_temp_co2) + scale_x_continuous(format="d")
plot_p = (
    base_plot
    + geom_line(aes(x="Year", y="Dec"), size=1)
    + labs(title="Dec temperature anomalies")
)
plot_q = (
    base_plot
    + geom_line(aes(x="Year", y="Trend"), size=1)
    + labs(title="Carbon dioxide emissions")
)
s=gggrid([plot_p, plot_q], ncol=2)
ggsave(s, filename="Anomalias_Emisiones_Diciembre.png", path=carpeta_destino)

#Coeficiente correlación Diciembre
correlacion_dec = df_temp_co2[["Dec", "Trend"]].corr(method="pearson")
print(correlacion_dec)

#Gráfica niveles CO2 anuales

base_plot = ggplot(df_temp_co2) + scale_x_continuous(format="d")
plot_p = (
    base_plot
    + geom_line(aes(x="Year", y="J-D"), size=1)
    + labs(title="J-D temperature anomalies")
)
plot_q = (
    base_plot
    + geom_line(aes(x="Year", y="Trend"), size=1)
    + labs(title="Carbon dioxide emissions")
)
m=gggrid([plot_p, plot_q], ncol=2)
ggsave(m, filename="Anomalias_Emisiones_Anuales.png", path=carpeta_destino)



