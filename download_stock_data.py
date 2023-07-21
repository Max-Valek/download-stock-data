import pandas as pd
import requests
import io
import os
from download_errors import handle_request_error, handle_parsing_error


def make_request(url):
    """Makes a GET request and returns the response.

    Parameters
    ----------
    url : str
        The URL string to send the request to.

    Returns
    -------
    response
        The HTTP response from the URL
    """

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()     # raise an exception for non-2xx status codes
        return response
    except Exception as e:
        handle_request_error(e)


def get_existing_data(save_path):
    """Get a DataFrame containing previously downloaded data for the ticker.

    Parameters
    ----------
    save_path : path
        Location to save the file.

    Returns
    -------
    DataFrame
        A DataFrame containing existing data, or an empty DataFrame.
    """

    if os.path.exists(save_path):
        return pd.read_csv(save_path)
    return pd.DataFrame()


def fetch_ticker_data(ticker):
    """Fetch ticker from Yahoo Finance API and return it as a DataFrame.

    Parameters
    ----------
    ticker : str
        Stock ticker to download data for (ex. AAPL).

    Returns
    -------
    DataFrame
        A DataFrame containing fetched stock data.
    """

    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1=0&period2=9999999999&interval=1d&events=history"
    response_text = make_request(url).text.strip()
    return pd.read_csv(io.StringIO(response_text))


def save_data(new, old, folder, filename):
    """Update or create CSV file for the stock.

    Parameters
    ----------
    new : DataFrame
        DataFrame of fetched entries not already in the file.
    old : DataFrame
        DataFrame containing the existing data in the file.
    folder: str
        The folder to save the file.
    filename: str
        The name of the file.
    """

    save_path = os.path.join(folder, filename)    # path for data file
    if not new.empty:
        if os.path.exists(save_path) and not old.empty:
            new = pd.concat([new, old], ignore_index=True)  # Concatenate existing and new data
        new = new.sort_values(by='Date', ascending=False)  # Sort by the 'Date' column in descending order
        new.to_csv(save_path, index=False)
        print(f"New entries added for {filename}. CSV file saved as {save_path}")
    else:
        print(f"No new entries found for {filename}. CSV file remains unchanged.")


def download(ticker, save_folder, save_filename):
    """Fetch data for a stock and save it as a CSV file, update the file if one exists.

    Parameters
    ----------
    ticker : str
        The stock ticker to download data for (ex. AAPL).
    save_folder: str
        The folder to save the file.
    save_filename: str
        The name of the file.
    """

    save_path = os.path.join(save_folder, save_filename)    # path for csv file
    existing_df = get_existing_data(save_path)              # existing data in file

    last_date = pd.Timestamp(0)                             # default value for last_date (1-1-1970)
    if not existing_df.empty:
        existing_df['Date'] = pd.to_datetime(existing_df['Date'])  # Convert 'Date' column to datetime type
        last_date = existing_df['Date'].max()                      # most recent entry in existing file

    try:
        new_df = fetch_ticker_data(ticker)                  # dataframe containing all returned data for the ticker
        new_df['Date'] = pd.to_datetime(new_df['Date'])     # convert Date column to datetime type
        new_df = new_df[new_df['Date'] > last_date]         # only new entries

        save_data(new_df, existing_df, save_folder, save_filename)

    except pd.errors.ParserError as e:
        handle_parsing_error(e)
