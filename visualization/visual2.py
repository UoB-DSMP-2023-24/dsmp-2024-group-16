import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv('C:/Users/Wilson/Desktop/TB2/Dataminiproject/Tape.csv')


plt.figure(figsize=(10, 6))
plt.scatter(data['Volume'], data['Open'], label='Volume vs Open')
plt.scatter(data['Volume'], data['High'], label='Volume vs High')
plt.scatter(data['Volume'], data['Low'], label='Volume vs Low')
plt.scatter(data['Volume'], data['Close'], label='Volume vs Close')


plt.legend()


plt.title('Volume and Price Relationships')
plt.xlabel('Volume')
plt.ylabel('Price')


plt.show()
