import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
ma_period = 360
df = pd.read_csv("data.csv")
df["MA"] = df["CloseValue"].rolling(window=ma_period).mean()
buy_point=0
buy_cols = [False]*len(df)

df["start_buy_point"] = (df["CloseValue"] < df["MA"]) & (df["CloseValue"].shift(1) > df["MA"].shift(1))
for i, d in enumerate(df["start_buy_point"]):
    if(d):
        buy_point=i
        for j in range(i, len(df)):
            if df["CloseValue"][j] < df["CloseValue"][buy_point] * 0.99:
                buy_cols[j] = True
                buy_point = j


df["buy"] = buy_cols
#print(df[df["buy"]]["CloseValue"])

selled_count=0
not_selled_count=0
sell_cols = [False]*len(df)
not_sell_cols = [False]*len(df)

close = df["CloseValue"]

for i, d in enumerate(df["buy"]):
    if(d):
        selled = False
        for j in range(i,len(df)):
            if(close[j] > close[i]*1.03):
                sell_cols[j]=True
                selled = True
                break
        if selled:
            selled_count += 1
        else:
            not_selled_count +=1
            not_sell_cols[i]=True

df["sell"] = sell_cols

print(selled_count)
print(not_selled_count)

plt.plot(close)
plt.plot(df["MA"])
for i, d in enumerate(df["buy"]):
    if(d):
        plt.scatter(i,close[i],c="r")
for i, d in enumerate(df["start_buy_point"]):
    if(d):
        plt.scatter(i,close[i],c="b")
for i, d in enumerate(not_sell_cols):
    if(d):
        plt.scatter(i,close[i],c="black")
plt.show()


