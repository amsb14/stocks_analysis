import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import pytz

def adjust_for_weekend(date, market="US"):
    """
    Adjusts the date to ensure it's a weekday. If the market is 'KSA', 
    adjusts for the Saudi market weekend (Friday and Saturday).
    For the 'US', adjusts for the US market weekend (Saturday and Sunday).
    """
    if market.upper() == "KSA":
        if date.weekday() == 4:  # Friday in KSA
            return date - timedelta(days=1)  # Move to Thursday
        elif date.weekday() == 5:  # Saturday in KSA
            return date + timedelta(days=2)  # Move to Sunday
    elif market.upper() == "US":
        if date.weekday() == 5:  # Saturday in US
            return date - timedelta(days=1)  # Move to Friday
        elif date.weekday() == 6:  # Sunday in US
            return date + timedelta(days=1)  # Move to Monday
    return date


    
def get_prices(ticker):
    market = "KSA" if ticker.endswith(".SR") else "US"
    stock = yf.Ticker(ticker)
    
    # Fetch stock information including industry and sector
    stock_info = stock.info
    industry = stock_info.get('industry', 'N/A')
    sector = stock_info.get('sector', 'N/A')
    name = stock_info.get('shortName', 'N/A')
    
    hist_maxi = stock.history(period="max")
    

    
    # Fetch the most recent price
    recent_hist = stock.history(period="1d")
    recent_price = recent_hist['Close'].iloc[0] if not recent_hist.empty else None
    
    # Determine dates for recent, 12 weeks ago, 24 weeks ago, and 1 year ago adjusted for weekend
    today = datetime.today().date()
    three_months = adjust_for_weekend(today - timedelta(days=90), market)
    six_months = adjust_for_weekend(today - timedelta(days=180), market)
    one_year = adjust_for_weekend(today - timedelta(days=365), market)
    
    close_price_three_months_ago = hist_maxi.loc[str(three_months)]['Close'] if str(three_months) in hist_maxi.index else "N/A"
    close_price_six_months_ago = hist_maxi.loc[str(six_months)]['Close'] if str(six_months) in hist_maxi.index else "N/A"
    close_price_one_year_ago = hist_maxi.loc[str(one_year)]['Close'] if str(one_year) in hist_maxi.index else "N/A"


    
    return {
    'Ticker': ticker,
    'Name': name,
    'Industry': industry,
    'Sector': sector,
    'Recent Price':f"{recent_price:.2f}" if isinstance(recent_price, (int, float)) else recent_price,
    'Close Price 3 Months Ago': f"{close_price_three_months_ago:.2f}" if isinstance(close_price_three_months_ago, (int, float)) else close_price_three_months_ago,
    'Close Price 6 Months Ago': f"{close_price_six_months_ago:.2f}" if isinstance(close_price_six_months_ago, (int, float)) else close_price_six_months_ago,
    'Close Price 1 Year Ago': f"{close_price_one_year_ago:.2f}" if isinstance(close_price_one_year_ago, (int, float)) else close_price_one_year_ago,

    }


# Define your list of companies' ticker symbols


def fetch_data_by_segment(companies, segment):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_prices, companies))
        df = pd.DataFrame(results)
        # Handle missing or 'N/A' values in 'Recent Price', 'Close Price 3 Months Ago', and 'Industry'
        df['Recent Price'] = pd.to_numeric(df['Recent Price'], errors='coerce')  # Convert 'Recent Price' to float, handle non-numeric
        df['Close Price 3 Months Ago'] = pd.to_numeric(df['Close Price 3 Months Ago'], errors='coerce')  # Convert 'Close Price 3 Months Ago' to float, handle non-numeric
        df['Close Price 6 Months Ago'] = pd.to_numeric(df['Close Price 6 Months Ago'], errors='coerce')  # Convert 'Close Price 3 Months Ago' to float, handle non-numeric
        df['Close Price 1 Year Ago'] = pd.to_numeric(df['Close Price 1 Year Ago'], errors='coerce')  # Convert 'Close Price 3 Months Ago' to float, handle non-numeric
        
        df = df[df[segment] != 'N/A']  # Filter out rows where 'Industry' is 'N/A'
        # Calculate the percentage change for each stock and create a new column
        df['Percent Change in 3 Months'] = ((df['Recent Price'] - df['Close Price 3 Months Ago']) / df['Close Price 3 Months Ago']) * 100
        df['Percent Change in 6 Months'] = ((df['Recent Price'] - df['Close Price 6 Months Ago']) / df['Close Price 6 Months Ago']) * 100
        df['Percent Change in 1 Year'] = ((df['Recent Price'] - df['Close Price 1 Year Ago']) / df['Close Price 1 Year Ago']) * 100
        # Round the 'Percent Change in 3 Months' to two decimal places
        df['Percent Change in 3 Months'] = df['Percent Change in 3 Months'].round(2)
        df['Percent Change in 6 Months'] = df['Percent Change in 6 Months'].round(2)
        df['Percent Change in 1 Year'] = df['Percent Change in 1 Year'].round(2)

        # Group by 'Industry' and sum up 'Recent Price' and 'Close Price 3 Months Ago' correctly
        segment_price_sum = df.groupby(segment).agg({
            'Recent Price': 'sum',
            'Close Price 3 Months Ago': 'sum',
            'Percent Change in 3 Months': 'mean',  # You might want to calculate the mean percentage change per industry
            'Close Price 6 Months Ago': 'sum',
            'Percent Change in 6 Months': 'mean',
            'Close Price 1 Year Ago': 'sum',
            'Percent Change in 1 Year': 'mean'
        }).reset_index()
        
        # Export DataFrame to Excel or display

        return segment_price_sum




