from prophet import Prophet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
df = df.rename(columns = {"StartDateTime":"ds","CloseValue":"y"})
df["ds"] = pd.to_datetime(df["ds"])

df_test=df[0:-50]

m = Prophet() # the Prophet class (model)
#m.add_seasonality(name='hourly', period=1/24, fourier_order=5)
m.fit(df_test) # fit the model using all data


future = m.make_future_dataframe(periods=50, freq='60min') #we need to specify the number of days in future
prediction = m.predict(future)

print(df_test)
print(prediction)
print(df)

plt.figure()
plt.plot(df["ds"],df["y"])
plt.plot(prediction["ds"],prediction["yhat"], color="red")
#plt.plot(df_test["ds"],df_test["y"], color="red")
# m.plot(prediction)

plt.title("Prediction of the Tesla Stock Price using the Prophet")
plt.xlabel("Date")
plt.ylabel("Close Stock Price")
plt.show()