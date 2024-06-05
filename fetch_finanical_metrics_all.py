import yfinance as yf
import pandas as pd

def fetch_and_transform_financials(ticker):
    """
    Fetches financial statements for a given ticker, transforms them to have metrics as columns,
    and returns a single DataFrame with one row per year and metrics as columns.
    """
    try:
        stock = yf.Ticker(ticker)
        # Fetch financial statements
        income_stmt = stock.income_stmt
        balance_sheet = stock.balance_sheet
        cash_flow = stock.cash_flow

        # Extract the company info
        info = stock.info
        company_info = {
            'Ticker Symbol': ticker,
            'Company Name': info.get('shortName', 'N/A'),
            'Industry': info.get('industry', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Recent Price': info.get('currentPrice', 'N/A'),  # Safely fetch currentPrice
        }

        # Transform each financial statement
        def transform_statement(statement, label_prefix):
            df = statement.copy()
            df = df.transpose()
            df.index = df.index.year  # Convert DatetimeIndex to just the year
            df.columns = [f"{label_prefix}: {col}" for col in df.columns]  # Prefix columns with statement label
            df['Year'] = df.index
            return df.reset_index(drop=True)

        income_stmt_df = transform_statement(income_stmt, 'Income Statement')
        balance_sheet_df = transform_statement(balance_sheet, 'Balance Sheet')
        cash_flow_df = transform_statement(cash_flow, 'Cash Flow')

        # Merge the transformed DataFrames on 'Year'
        merged_df = pd.merge(pd.merge(income_stmt_df, balance_sheet_df, on='Year', how='outer'), cash_flow_df, on='Year', how='outer')
        
        # Add company info to merged DataFrame
        for key, value in company_info.items():
            merged_df[key] = value
        
        # Ensure the order of the company info columns
        final_columns = ['Ticker Symbol', 'Company Name', 'Industry', 'Sector', 'Year', 'Recent Price'] + [col for col in merged_df.columns if col not in ['Ticker Symbol', 'Company Name', 'Industry', 'Sector', 'Year','Recent Price']]
        return merged_df[final_columns]

    except Exception as e:
        print(f"Failed to fetch or transform data for {ticker}. Error: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of error

def aggregate_financials(tickers):
    """
    Aggregates transformed financials for a list of tickers into a single DataFrame.
    """
    aggregated_df = pd.DataFrame()
    for ticker in tickers:
        df = fetch_and_transform_financials(ticker)
        if not df.empty:
            aggregated_df = pd.concat([aggregated_df, df], ignore_index=True)
    
    # Export to Excel
    output_path = "aggregated_financials_transformed.xlsx"
    aggregated_df.to_excel(output_path, index=False)
    
    return aggregated_df
