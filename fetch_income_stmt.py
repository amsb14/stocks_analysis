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
    stock = yf.Ticker(ticker)  # Adjusted for market
    
    # Fetch stock information including industry and sector
    stock_info = stock.info
    industry = stock_info.get('industry', 'N/A')
    sector = stock_info.get('sector', 'N/A')
    name = stock_info.get('shortName', 'N/A')
    
    # Fetch the last 3 to 4 years from the income statement
    recent_years = stock.income_stmt.columns[-4:][::-1] # Get the last 4 columns
    financial_metrics = {}
    metrics_of_interest = ["Total Revenue", "Gross Profit", "Operating Income", "Net Income", "Diluted EPS"]

    for metric in metrics_of_interest:
        for year in range(4):
            year_label = f"{metric.replace(' ', '')}_{datetime.now().year - (4-year)}"
            try:
                year_col = recent_years[year]
                if metric in stock.income_stmt.index:
                    financial_metrics[year_label] = stock.income_stmt.loc[metric, year_col]
                else:
                    # Metric not found, mark as N/A
                    financial_metrics[year_label] = "N/A"
            except IndexError:
                # If the year does not exist, mark as N/A
                financial_metrics[year_label] = "N/A"
    
    return {
        'Ticker': ticker,
        'Name': name,
        'Industry': industry,
        'Sector': sector,
        **financial_metrics  # Expand the revenue_data dictionary into the return dictionary
    }


# Define your list of companies' ticker symbols
def fetch_data_income_stmt(companies):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_prices, companies))
    return pd.DataFrame(results)

