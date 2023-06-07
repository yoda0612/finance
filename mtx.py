import pandas as pd
import matplotlib.pyplot as plt
import  numpy as np
ma_period=60
df = pd.read_csv("Min60.csv")

for ma_period in range(5,240):
    df["MA"] = df["Close"].rolling(window=ma_period).mean()

    crossUp = [False] * len(df)

    df["CrossUp"] = (df["Close"] > df["MA"]) & (df["Close"] < df["MA"]).shift(1)
    df["CrossDown"] = (df["Close"] < df["MA"]) & (df["Close"] > df["MA"]).shift(1)

    # print(df[df["CrossUp"]])
    # print(df[df["CrossDown"]])

    rateList = []

    for i in range(len(df)):
        if df.loc[i]["CrossUp"]:
            for j in range(i, len(df)):
                if df.loc[j]["CrossDown"]:
                    max = df.loc[i + 1:j, "Close"].max()
                    start = df.loc[i, "Close"]
                    rate = max / start
                    rateList.append(rate)
                    # print(start, max, rate)
                    break

    print(ma_period,np.array(rateList).mean(), np.array(rateList).max(),np.array(rateList).min())
# #df = df.tail(500)
# df = df.reset_index()
# print(df)
# plt.figure()
# plt.plot(df["Close"])
# plt.plot(df["MA"])
#
# for i in range(len(df)):
#     print(i)
#     if df.loc[i]["CrossUp"]:
#         plt.scatter(i,df.loc[i]["Close"], color="red")
#     if df.loc[i]["CrossDown"]:
#        plt.scatter(i, df.loc[i]["Close"], color="green")
# plt.show()



