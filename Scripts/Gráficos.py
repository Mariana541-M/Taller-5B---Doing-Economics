import pandas as pd
import matplotlib as npl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import pingouin as pg
from lets_plot import *

LetsPlot.setup_html(no_js=True)

### You don't need to use these settings yourself,
### they are just here to make the charts look nicer!
# Set the plot style for prettier charts:
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
"//////////////////////////////////////"
month = "J-D"
fig, ax = plt.subplots()
ax.axhline(0, color="green")
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[month].plot(ax=ax)
ax.set_title(
    f"Average temperature anomaly in {month} \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");
"/////////////////"
estaciones=["DJF","MAM","JJA","SON"]
fig, ax = plt.subplots()
ax.axhline(0, color="black")
ax.annotate("1951—1980 average", xy=(0.66, -0.2), xycoords=("figure fraction", "data"))
df[estaciones].plot(ax=ax)
ax.set_title(
    f"Average temperature anomaly by season \n in the northern hemisphere (1880—{df.index.max()})"
)
ax.set_ylabel("Annual temperature anomalies");