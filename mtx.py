import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# for m in range(1,121):
#     with open("Min"+str(m)+".csv","r") as fr:
#         with open("Min" + str(m) + ".tmp", "w") as fw:
#             fw.write("Date,Open,High,Low,Close,Volume\n")
#             for line in fr.readlines():
#                 fw.write(line)
#
#     os.remove("Min"+str(m)+".csv")
#     os.rename("Min" + str(m) + ".tmp", "Min"+str(m)+".csv")

def get_result(file_number, ma_period):
    df = pd.read_csv("Min"+ str(file_number)+".csv")
    df["MA"] = df["Close"].rolling(window=ma_period).mean()
    df["CrossUp"] = (df["Close"] > df["MA"]) & (df["Close"] < df["MA"]).shift(1)
    df["CrossDown"] = (df["Close"] < df["MA"]) & (df["Close"] > df["MA"]).shift(1)

    rateList = []

    file_index=1
    for i in range(len(df)):
        if df.loc[i]["CrossUp"]:
            for j in range(i, len(df)):
                if df.loc[j]["CrossDown"]:
                    max = df.loc[i + 1:j, "Close"].max()
                    start = df.loc[i, "Close"]
                    rate = max / start
                    rateList.append(rate)

                    print(df.loc[i:j, ["Date","Close","MA"]])
                    df.loc[i:j, ["Date", "Close", "MA"]].to_csv("result_"+str(file_index)+".csv")
                    file_index+=1

                    break

    return np.array(rateList).mean(), np.array(rateList).max(), np.array(rateList).min()

get_result(64,46)

# result_all=[]
#
# for m in range(1,121):
#     result_row = []
#
#     for ma_period in range(5, 121):
#         print(m, ma_period)
#         result_row.append(get_result(m, ma_period))
#
#     result_all.append(result_row)
#
# with open("mean.csv","w") as f:
#     with open("max.csv", "w") as f_max:
#         with open("min.csv", "w") as f_min:
#             for row in result_all:
#                 for mean, max, min in row:
#                     f.write(str(mean) + ",")
#                     f_max.write(str(max) + ",")
#                     f_min.write(str(min) + ",")
#                 f.write("\n")
#                 f_max.write("\n")
#                 f_min.write("\n")



# ma_period=60
# df = pd.read_csv("Min60.csv")
#
# for ma_period in range(5,240):
#     df["MA"] = df["Close"].rolling(window=ma_period).mean()
#
#     crossUp = [False] * len(df)
#
#     df["CrossUp"] = (df["Close"] > df["MA"]) & (df["Close"] < df["MA"]).shift(1)
#     df["CrossDown"] = (df["Close"] < df["MA"]) & (df["Close"] > df["MA"]).shift(1)
#
#     # print(df[df["CrossUp"]])
#     # print(df[df["CrossDown"]])
#
#     rateList = []
#
#     for i in range(len(df)):
#         if df.loc[i]["CrossUp"]:
#             for j in range(i, len(df)):
#                 if df.loc[j]["CrossDown"]:
#                     max = df.loc[i + 1:j, "Close"].max()
#                     start = df.loc[i, "Close"]
#                     rate = max / start
#                     rateList.append(rate)
#                     # print(start, max, rate)
#                     break
#
#     print(ma_period,np.array(rateList).mean(), np.array(rateList).max(),np.array(rateList).min())
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



