import yfinance as yf
import pandas as pd

def fetch_and_transform_financials(ticker):
    """
    Fetches quarterly financial statements for a given ticker, transforms them to have metrics as columns,
    and returns a single DataFrame with one row per quarter and metrics as columns.
    """
    stock = yf.Ticker(ticker)
    # Fetch quarterly financial statements 
    income_stmt = stock.quarterly_income_stmt
    balance_sheet = stock.quarterly_balance_sheet
    cash_flow = stock.quarterly_cash_flow

    # Extract the company info
    info = stock.info
    recent_price = info['currentPrice']
    
    company_info = {
        'Ticker Symbol': ticker,
        'Company Name': info.get('shortName', 'N/A'),
        'Industry': info.get('industry', 'N/A'),
        'Sector': info.get('sector', 'N/A'),
        'Recent Price': info.get('currentPrice', 'N/A'),
    }

    # Function to transform and label DataFrame
    def transform_statement(statement, label_prefix):
        df = statement.copy()
        df = df.transpose()
        df.index = pd.to_datetime(df.index).to_period('Q')  # Convert DatetimeIndex to Quarter
        df.columns = [f"{label_prefix}: {col}" for col in df.columns]  # Prefix columns with statement label
        df['Quarter'] = df.index
        return df.reset_index(drop=True)

    # Transform each financial statement
    income_stmt_df = transform_statement(income_stmt, 'Income Statement')
    balance_sheet_df = transform_statement(balance_sheet, 'Balance Sheet')
    cash_flow_df = transform_statement(cash_flow, 'Cash Flow')

    # Merge the transformed DataFrames on 'Quarter'
    merged_df = pd.merge(pd.merge(income_stmt_df, balance_sheet_df, on='Quarter', how='outer'), cash_flow_df, on='Quarter', how='outer')
    
    # Add company info to merged DataFrame
    for key, value in company_info.items():
        merged_df[key] = value
    
    # Ensure the order of the company info columns
    final_columns = ['Ticker Symbol', 'Company Name', 'Industry', 'Sector', 'Quarter', 'Recent Price'] + [col for col in merged_df.columns if col not in ['Ticker Symbol', 'Company Name', 'Industry', 'Sector', 'Quarter', 'Recent Price']]
    return merged_df[final_columns]

def aggregate_financials(tickers):
    """
    Aggregates transformed quarterly financials for a list of tickers into a single DataFrame.
    """
    aggregated_df = pd.DataFrame()
    for ticker in tickers:
        df = fetch_and_transform_financials(ticker)
        aggregated_df = pd.concat([aggregated_df, df], ignore_index=True)
    
    # Export to Excel
    output_path = "aggregated_quarterly_financials_transformed.xlsx"
    aggregated_df.to_excel(output_path, index=False)
    
    return aggregated_df
