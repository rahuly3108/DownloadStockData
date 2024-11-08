import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

data = pd.read_csv('ind_nifty200list.csv')
symbols_list = data['Symbol']
# Calculate the start date as one year ago from today
end_date = datetime.now()
start_date = end_date - timedelta(days=365)
all_stocks_df = pd.DataFrame()
# Loop through each stock symbol and download the adjusted close prices
for symbol in symbols_list:
    stock_df = yf.download(symbol + '.NS', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)['Adj Close'].reset_index()
    stock_df.columns = ['Date', symbol]
    stock_df['Date'] = stock_df['Date'].dt.date
    if all_stocks_df.empty:
        all_stocks_df = stock_df 
    else:
        all_stocks_df = pd.merge(all_stocks_df, stock_df, on='Date', how='outer')
# Download Nifty 50 data
nifty50_df = yf.download('^NSEI', start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)['Adj Close'].reset_index()
nifty50_df.columns = ['Date', 'Nifty50']
nifty50_df['Date'] = nifty50_df['Date'].dt.date
# Merge Nifty 50 data with all stocks DataFrame
all_stocks_df = pd.merge(all_stocks_df, nifty50_df, on='Date', how='outer')
all_stocks_df.to_csv('Stock_data.csv',index=False)


# In[ ]:




