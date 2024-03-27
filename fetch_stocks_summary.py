import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_stock_data(ticker_symbol):
    """
    Fetches financial metrics for a given stock ticker symbol.
    """
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        cashflow = stock.cashflow
        
        # Assuming 'Free Cash Flow' and 'Operating Cash Flow' are provided directly
        free_cash_flow_latest = cashflow.loc['Free Cash Flow'].iloc[0] if 'Free Cash Flow' in cashflow.index else 'N/A'
        operating_cash_flow_latest = cashflow.loc['Operating Cash Flow'].iloc[0] if 'Operating Cash Flow' in cashflow.index else 'N/A'
        
        return {
            'Ticker': ticker_symbol,
            'Company Name': info.get('shortName', 'N/A'),
            'Industry': info.get('industry', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'P/E Ratio': info.get('forwardPE'),
            'P/B Ratio': info.get('priceToBook'),
            'EV/EBITDA': info.get('enterpriseToEbitda'),
            'P/S Ratio': info.get('priceToSalesTrailing12Months'),
            'ROE': info.get('returnOnEquity'),
            'ROA': info.get('returnOnAssets'),
            'Gross Margin': info.get('grossMargins'),
            'Operating Margin': info.get('operatingMargins'),
            'Net Margin': info.get('profitMargins'),
            'Debt-to-Equity Ratio': info.get('debtToEquity'),
            'Current Ratio': info.get('currentRatio'),
            'Quick Ratio': info.get('quickRatio'),
            'Free Cash Flow': free_cash_flow_latest,
            'Operating Cash Flow': operating_cash_flow_latest,
            'Dividend Yield': info.get('dividendYield'),
            'Dividend Payout Ratio': info.get('payoutRatio'),
        }
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None

def fetch_summary(stocks):
    data = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_stock = {executor.submit(fetch_stock_data, stock): stock for stock in stocks}
        for future in as_completed(future_to_stock):
            stock_data = future.result()
            if stock_data:
                data.append(stock_data)
    
    # Convert the list of data to a pandas DataFrame and specify the columns order
    df = pd.DataFrame(data)
    columns_order = ['Ticker', 'Company Name', 'Industry', 'Sector', 'P/E Ratio', 'P/B Ratio', 
                     'EV/EBITDA', 'P/S Ratio', 'ROE', 'ROA', 'Gross Margin', 'Operating Margin', 
                     'Net Margin', 'Debt-to-Equity Ratio', 'Current Ratio', 'Quick Ratio', 
                     'Free Cash Flow', 'Operating Cash Flow', 'Dividend Yield', 'Dividend Payout Ratio']
    df = df[columns_order]
    
    return df

