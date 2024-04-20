import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def fetch_dividends_for_ticker(ticker, start_date, end_date):
    """
    Fetches dividends for a single ticker within the specified date range and the recent price (1 day ago).
    """
    stock = yf.Ticker(ticker)
    hist = stock.dividends.loc[start_date:end_date]
    annual_dividends = hist.resample('Y').sum()

    # Fetch the recent closing price (1 day ago)
    recent_price_data = stock.history(period="2d")  # Fetch data for the last 2 days to ensure we get '1d ago' price
    if len(recent_price_data['Close']) >= 2:
        recent_price = recent_price_data['Close'].iloc[-2]  # Get the closing price from the second last day
    else:
        recent_price = None  # Handle the case with less than 2 days of data

    # Fetch stock information
    info = stock.info
    stock_data = {
        'Ticker': ticker,
        'Name': info.get('shortName', ''),
        'Industry': info.get('industry', ''),
        'Sector': info.get('sector', ''),
        'Recent Price': recent_price,
    }

    # Add dividend data
    for year, dividend in annual_dividends.items():
        stock_data[str(year.year)] = dividend

    return stock_data

def fetch_dividends_and_info(tickers):
    """
    Fetches dividends for the past 5 years for a list of tickers along with stock information and the recent price (1 day ago).
    Implements threading to speed up the process.
    """
    end_date = pd.Timestamp.now().tz_localize(None)  # Ensure timezone-naive
    start_date = end_date - pd.DateOffset(years=5)

    columns = ['Ticker', 'Name', 'Industry', 'Sector', 'Recent Price'] + [str(year) for year in range(end_date.year - 5, end_date.year)]
    df = pd.DataFrame(columns=columns)

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_dividends_for_ticker, ticker, start_date, end_date) for ticker in tickers]
        for future in futures:
            df = df.append(future.result(), ignore_index=True)

    return df
