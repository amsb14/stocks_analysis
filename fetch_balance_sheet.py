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
    current_ratio = stock_info.get("currentRatio", "N/A")
    debt_to_equity = stock_info.get("debtToEquity", "N/A")
    return_on_equity = stock_info.get("returnOnEquity", "N/A")
    try:
        # Check if there are columns in both income_stmt and balance_sheet
        if not stock.income_stmt.columns.empty and not stock.balance_sheet.columns.empty:
            total_revenue = stock.income_stmt.loc["Total Revenue", stock.income_stmt.columns[0]] if "Total Revenue" in stock.income_stmt.index else 0
            total_assets = stock.balance_sheet.loc["Total Assets", stock.balance_sheet.columns[0]] if "Total Assets" in stock.balance_sheet.index else 0

            # Proceed with the calculation if total_assets is not zero
            asset_turnover = total_revenue / total_assets if total_assets != 0 else "N/A"
        else:
            # If there are no columns, set asset_turnover to "N/A"
            asset_turnover = "N/A"
    except KeyError:
        # If the necessary data is missing, set asset_turnover to "N/A"
        asset_turnover = "N/A"
    except ZeroDivisionError:
        # Handle any division by zero errors
        asset_turnover = "N/A"


    # Fetch the last 3 to 4 years from the income statement
    recent_years = stock.balance_sheet.columns[-4:][::-1] # Get the last 4 columns
    financial_metrics = {}
    metrics_of_interest = ["Current Assets", "Current Liabilities", "Working Capital"]

    for metric in metrics_of_interest:
        for year in range(4):
            year_label = f"{metric.replace(' ', '')}_{datetime.now().year - (4-year)}"
            try:
                year_col = recent_years[year]
                if metric in stock.balance_sheet.index:
                    financial_metrics[year_label] = stock.balance_sheet.loc[metric, year_col]
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
        **financial_metrics,  # Expand the revenue_data dictionary into the return dictionary
        "current_ratio": current_ratio,
        "debt_to_equity": debt_to_equity,
        "return_on_equity": return_on_equity,
        "Asset Turnover": asset_turnover
        

        
    }

# Define your list of companies' ticker symbols
def fetch_data_balance_sheet(companies):
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(get_prices, companies))
    return pd.DataFrame(results)


