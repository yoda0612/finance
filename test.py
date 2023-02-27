import pandas as pd
import mplfinance as mf
import talib
import numpy as np
import math
df = pd.read_csv("eth1h.csv")
df.index = pd.DatetimeIndex(df['StartTime'])
df=df.rename(columns={'HighValue': 'High', 'CloseValue': 'Close', 'LowValue': 'Low', 'OpenValue': 'Open','Volumn':'Volume'})
buy_signal=[np.nan]
last_buy_index=0
grid_period=30
thread_hole=0.01
current_grid_period=29
for i in range(1,len(df["Close"])):
    if (df["Close"][last_buy_index]-df["Close"][i])/df["Close"][last_buy_index] > thread_hole:
        last_buy_index=i
        buy_signal.append(df["Close"][i])
    else:
        buy_signal.append(np.nan)

    current_grid_period -= 1
    if current_grid_period == 0:
        last_buy_index = i
        current_grid_period = grid_period

#print(buy_signal[buy_signal!=0])


MA5=list(talib.MA(df["Close"],timeperiod=5,matype=0))
MA5[8:]=MA5[0:-8]
df["MA5"]=MA5

MA8=list(talib.MA(df["Close"],timeperiod=8,matype=0))
MA8[5]=MA8[0:-5]
df["MA8"]=MA8

MA13=list(talib.MA(df["Close"],timeperiod=13,matype=0))
MA13[3]=MA13[0:-3]
df["MA13"]=MA13

df["Buy"]=buy_signal

df=df[-600:]
print(df[df["Buy"]!=0][["Close","Buy"]])
MA5=mf.make_addplot(df["MA5"],color='green')
MA8=mf.make_addplot(df["MA8"],color='red')
MA13=mf.make_addplot(df["MA13"],color='blue')
buy = mf.make_addplot(df["Buy"],type='scatter',color='red')


increase_rate=0.05
total_increase=0
finished=0
total_buy=0
#print(math.isnan(df["Buy"][-1]))
for i in range(len(df)):
    if not math.isnan(df["Buy"][i]):
        total_buy+=1
        for j in range(i+1,len(df)):
            if (df["Close"][j]-df["Close"][i])/df["Close"][i] > increase_rate:
                total_increase += (df["Close"][j]-df["Close"][i])/df["Close"][i]
                length=j-i
                print((df["Close"][j]-df["Close"][i])/df["Close"][i],length)
                finished += 1
                break

print(total_increase)
print(total_buy)
print(finished)


mf.plot(df, type='line',  addplot=buy)



