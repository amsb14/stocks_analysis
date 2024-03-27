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

def assess_dividend_continuity(hist_dividends):
    # Simple analysis of dividend continuity
    prev_year_dividend = 0
    years_with_dividends = 0
    years_with_increases = 0
    for dividend in hist_dividends:
        if dividend > 0:
            years_with_dividends += 1
            if dividend > prev_year_dividend:
                years_with_increases += 1
        prev_year_dividend = dividend
    
    if years_with_dividends == len(hist_dividends) and years_with_increases > 0:
        return "High"
    elif years_with_dividends == len(hist_dividends):
        return "Moderate"
    else:
        return "Low"
    
def get_prices(ticker):
    

    market = "KSA" if ticker.endswith(".SR") else "US"
    # stock = yf.Ticker(ticker + ".SR") # SAUDI MARKET ONLY
    stock = yf.Ticker(ticker) # US MARKET ONLY
    
    # Fetch stock information including industry and sector
    stock_info = stock.info
    industry = stock_info.get('industry', 'N/A')
    sector = stock_info.get('sector', 'N/A')
    name = stock_info.get('shortName', 'N/A')
        
    try:
        # Your existing setup code here...
        start_date = (datetime.today() - timedelta(days=365*5)).replace(tzinfo=pytz.UTC)
    
        # Check if dividends series is not empty and has a DatetimeIndex before proceeding
        hist_dividends = stock.dividends[start_date:]
        if hist_dividends.empty or not isinstance(hist_dividends.index, pd.DatetimeIndex):
            print(f"No dividends data or inappropriate index for {ticker}. Skipping dividend analysis.")
            dividend_continuity = "N/A"  # or any other default value you see fit
        else:
            hist_dividends_grouped = hist_dividends.groupby(pd.Grouper(freq='Y')).sum()
            dividend_continuity = assess_dividend_continuity(hist_dividends_grouped)
        
        # Get the most recent dividend and its date
        if not stock.dividends.empty:
            last_dividend = stock.dividends.iloc[-1]
            last_dividend_date = stock.dividends.index[-1].date()
        else:
            last_dividend = "N/A"
            last_dividend_date = "N/A"
        
        # Determine dates for recent, 12 weeks ago, 24 weeks ago, and 1 year ago adjusted for weekend
        today = datetime.today().date()
        twelve_weeks_ago = adjust_for_weekend(today - timedelta(weeks=12), market)
        twenty_four_weeks_ago = adjust_for_weekend(today - timedelta(weeks=24), market)
        one_year_ago = adjust_for_weekend(today - timedelta(weeks=52), market)
        
        # Fetch historical data
        hist = stock.history(start=one_year_ago - timedelta(days=1), end=today)
        hist_maxi = stock.history(period="max")
        
        recent_price = hist['Close'].iloc[-1] if not hist.empty else None
        lowest_price = hist['Low'].min()
        highest_price = hist['High'].max()
        percentage_increase = ((recent_price - lowest_price) / lowest_price) if lowest_price else None
        percentage_decrease = ((highest_price - recent_price) / highest_price) if highest_price else None
        
        # Fetch close prices 12 weeks, 24 weeks ago, and 1 year ago
        close_price_12_weeks_ago = hist.loc[str(twelve_weeks_ago)]['Close'] if str(twelve_weeks_ago) in hist.index else "N/A"
        close_price_24_weeks_ago = hist.loc[str(twenty_four_weeks_ago)]['Close'] if str(twenty_four_weeks_ago) in hist.index else "N/A"
        close_price_1_year_ago = hist.loc[str(one_year_ago)]['Close'] if str(one_year_ago) in hist.index else "N/A"
    
        historical_high = hist_maxi['Close'].max()
        historical_low = hist_maxi['Close'].min()
        
        # Calculate the 50-day moving average of the closing prices
        fifty_day_ma = hist['Close'].rolling(window=50).mean()
        twohundred_day_ma = hist['Close'].rolling(window=200).mean()
        
        
        # Calculate total adjusted dividends for the last 12 months
        total_dividends_last_12_months = stock.info.get('trailingAnnualDividendRate', "N/A")
    
    
        
        
        return {
        'Ticker': ticker,
        'Name': name,
        'Industry': industry,
        'Sector': sector,
        'Recent Price': f"{recent_price:.2f}" if isinstance(recent_price, (int, float)) else recent_price,
        'Lowest Price in 52 Weeks': f"{lowest_price:.2f}" if isinstance(lowest_price, (int, float)) else lowest_price,
        '% Increase from Low': f"{percentage_increase:.2f}" if isinstance(percentage_increase, (int, float)) else percentage_increase,
        'Highest Price in 52 Weeks': f"{highest_price:.2f}" if isinstance(highest_price, (int, float)) else highest_price,
        '% Decrease from High': f"{percentage_decrease:.2f}" if isinstance(percentage_decrease, (int, float)) else percentage_decrease,
        'Close Price 12 Weeks Ago': f"{close_price_12_weeks_ago:.2f}" if isinstance(close_price_12_weeks_ago, (int, float)) else close_price_12_weeks_ago,
        'Close Price 24 Weeks Ago': f"{close_price_24_weeks_ago:.2f}" if isinstance(close_price_24_weeks_ago, (int, float)) else close_price_24_weeks_ago,
        'Close Price 1 Year Ago': f"{close_price_1_year_ago:.2f}" if isinstance(close_price_1_year_ago, (int, float)) else close_price_1_year_ago,
        'Historical High Close': f"{historical_high:.2f}" if historical_high else "N/A",
        'Historical Low Close': f"{historical_low:.2f}" if historical_low else "N/A",
        "50-Day MA": f"{fifty_day_ma.iloc[-1]:.2f}" if not fifty_day_ma.empty else "N/A",  # Correct access to the most recent 50-day MA
        "200-Day MA": f"{twohundred_day_ma.iloc[-1]:.2f}" if not twohundred_day_ma.empty else "N/A",  # Correct access to the most recent 200-day MA
        "Total Adjusted Dividends Last 12 Months": f"{total_dividends_last_12_months:.2f}" if total_dividends_last_12_months != "N/A" else total_dividends_last_12_months,
        'Dividend Continuity': dividend_continuity,
        'Last Dividend': last_dividend if last_dividend != "N/A" else "N/A",
        'Last Dividend Date': last_dividend_date if last_dividend_date != "N/A" else "N/A",
        }

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return {
            # Handle the error case...
        }


# Define your list of companies' ticker symbols
def fetch_prices(companies):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_prices, companies))
    return pd.DataFrame(results)


print("Data exported to price_stats_compare.xlsx")
