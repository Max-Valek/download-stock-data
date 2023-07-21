import os
import argparse
from download_stock_data import download
from download_errors import DownloadError, ParsingError, RequestError, handle_request_error, handle_parsing_error

# View CSV as a table: right click file, open with the extension

if __name__ == "__main__":
    # Handle arguments
    parser = argparse.ArgumentParser(description="Download historical stock data for a specified ticker")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL, GOOG) for which to download the data.")
    args = parser.parse_args()

    # Location to store CSV file for the ticker data.
    folder_name = "data"
    file_name = f"{args.ticker}.csv"

    # Create the data folder if it doesn't already exist.
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Download and save ticker data from Yahoo Finance API.
    try:
        download(args.ticker, folder_name, file_name)
    except DownloadError as e:
        print(e)
    except RequestError as e:
        print(e)
    except ParsingError as e:
        print(e)
