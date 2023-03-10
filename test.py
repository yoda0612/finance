import pandas as pd
import mplfinance as mf
import talib
import numpy as np
import math
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

import matplotlib.pyplot as plt

# X=np.arange(7)
# X=preprocessing.normalize([X]).reshape(-1,1)
# print(X)
# y=np.array([1968.09,2096.39,2141.29,2291.1,2367.74,2509.07,2650.86])
# y=preprocessing.normalize([y]).reshape(-1)
# print(y)
# reg = LinearRegression().fit(X, y)
# y_pred=reg.predict(X)
# print(reg.coef_)
# plt.plot(y)
# plt.plot(y_pred)
# plt.show()
# exit()
def Regression(Close, timeperiod=7):
    Close=Close.to_numpy()
    result = [np.nan] * len(Close)
    #X=np.arange(timeperiod).reshape(-1,1)
    X = np.arange(timeperiod)
    X = preprocessing.normalize([X]).reshape(-1, 1)
    for i in range(timeperiod-1,len(Close)):
        y=Close[i-timeperiod+1:i+1]
        y=preprocessing.normalize([y]).reshape(-1)
        reg = LinearRegression().fit(X, y)
        result[i]=reg.coef_[0]

        if reg.coef_[0] > 100:
            print(y)

    return result

df = pd.read_csv("eth4h.csv")
df.index = pd.DatetimeIndex(df['StartTime'])
df=df.rename(columns={'HighValue': 'High', 'CloseValue': 'Close', 'LowValue': 'Low', 'OpenValue': 'Open','Volumn':'Volume'})

reg=Regression(df["Close"],timeperiod=14)
df["reg"]=reg

buy_signal=[np.nan]
last_buy_index=0
grid_period=30
thread_hole=0.01
current_grid_period=grid_period-1
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

df=df[-50:]
MA5=mf.make_addplot(df["MA5"],color='green')
MA8=mf.make_addplot(df["MA8"],color='red')
MA13=mf.make_addplot(df["MA13"],color='blue')
reg=mf.make_addplot(df["reg"],color='blue', panel=1)

buy = mf.make_addplot(df["Buy"],type='scatter',color='red')


increase_rate=0.01
total_increase=0
finished=0
total_buy=0
unsuccessful=[np.nan] * len(df)
money = 1000
total_money = 0
for i in range(len(df)):
    if not math.isnan(df["Buy"][i]):
        total_buy+=1
        successful=False
        for j in range(i+1,len(df)):
            if (df["Close"][j]-df["Close"][i])/df["Close"][i] > increase_rate:
                total_increase += (df["Close"][j]-df["Close"][i])/df["Close"][i]
                length=j-i
                days = int(length / 24)
                hours = length - days * 24
                total_money += ((df["Close"][j] - df["Close"][i]) / df["Close"][i]) * money
                print((df["Close"][j]-df["Close"][i])/df["Close"][i],days, hours, total_increase)
                finished += 1
                successful=True
                break
        if successful:
            unsuccessful[i] = np.nan
        else:
            unsuccessful[i] = df["Close"][i]
df["unsuccessful"] = unsuccessful
print(total_increase)
print(total_buy)
print(finished)
print(total_money)
unsuccessful = mf.make_addplot(df["unsuccessful"],type='scatter',color='green')

mf.plot(df, type='line',  addplot=[buy, unsuccessful,reg])



