import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

ticker = 'AAPL'
start_date = '2017-01-01'
end_date = '2024-09-06'
interval = '7d'
amount = 5

data = yf.download(ticker, start_date, end_date)

data = data.dropna()

resampled_data = data.resample(interval).first()


total_investment = 0
total_shares = 0

dca_log = []

for date, row in resampled_data.iterrows():
    price = row['Adj Close']
    shares_bought = amount / price
    total_shares += shares_bought
    total_investment += amount

    dca_log.append({
        'Date': date,
        'Price': price,
        'Total Shares': total_shares,
        'Total Investment': total_investment,
        'Portfolio Value': total_shares * price
    })

dca_df = pd.DataFrame(dca_log)

final_portfolio_value = total_shares * data.iloc[-1]['Adj Close']
total_profit = final_portfolio_value - total_investment

plt.figure(figsize=(10, 6))
plt.plot(dca_df['Date'], dca_df['Portfolio Value'], label='Portfolio Value')
plt.plot(dca_df['Date'], dca_df['Total Investment'], label='Invested Amount')
plt.xlabel('Date')
plt.ylabel('Value in $')
plt.title(f'Dollar Cost Averaging for {ticker}')
plt.legend()
plt.grid()
plt.show()