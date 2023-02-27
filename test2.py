import pandas as pd
import matplotlib.pyplot as plt

def covertToFloat(df,columns):
    for c in columns:
        df[c] = df[c].str.replace("$", "").replace(",", "")
        df[c] = df[c].str.replace(",", "")
        df[c] = df[c].str.strip()
        df[c] = df[c].astype(float)
    return  df

df = pd.read_csv("ETH結構理財抄底寶.csv")


old_col_names = list(df.columns)
new_col_names = [x.strip() for x in old_col_names]
new_names = dict(zip(old_col_names,new_col_names))
df.rename(columns=new_names,inplace=True)
df = df[["系統時間","開盤價","最高價","最低價","收盤價","成交量","區段低點","區段高點","區段支撐","區段均價","區段阻力"]]
df=df[~df["系統時間"].isnull()]
df=df[-100:]

df = covertToFloat(df,["開盤價","最高價","最低價","收盤價","區段低點","區段高點","區段支撐","區段均價","區段阻力"])

print(df)

plt.plot(df["收盤價"],label="Close")
plt.plot(df["區段低點"],label="IntervalLow")
plt.plot(df["區段高點"],label="IntervalHigh")
plt.plot(df["區段支撐"],label="Support")
plt.plot(df["區段均價"],label="Avg")
plt.plot(df["區段阻力"],label="Resistance")
plt.legend()
plt.show()

