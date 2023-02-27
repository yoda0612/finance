from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import mplfinance as mf
import talib
import numpy as np
import math
from talib import abstract
import matplotlib.pyplot as plt

df = pd.read_csv("eth.csv")
df.index = pd.DatetimeIndex(df['StartTime'])
df=df.rename(columns={'HighValue': 'high', 'CloseValue': 'close', 'LowValue': 'low', 'OpenValue': 'open','Volumn':'volume'})
for recongniter in talib.get_function_groups()['Pattern Recognition']:
    df[recongniter] = getattr(abstract, recongniter)(df)
print(df)
print(df[talib.get_function_groups()['Pattern Recognition']].to_numpy())
data = df[talib.get_function_groups()['Pattern Recognition']].to_numpy()

kmeans = KMeans(n_clusters=2, random_state=0, n_init=10).fit(data)
df["label"]=kmeans.labels_
cdict = {0: 'red', 1: 'blue', 3: 'green'}
df=df[-100:]
plt.plot(np.arange(len(df)),df["close"])
for i, d in enumerate(df["close"]):
    plt.scatter(i, d,c=cdict[df["label"][i]], label=df["label"][i])
plt.show()
