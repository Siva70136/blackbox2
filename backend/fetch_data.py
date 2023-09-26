import yfinance as yf
from pymongo import MongoClient
from datetime import datetime, timedelta

def fetch_and_store_data():
    # Data fetching and storing logic here
    client = MongoClient("mongodb+srv://siva:L7vTobLaY5ndDoaY@cluster0.6nug7fa.mongodb.net/?retryWrites=true&w=majority")
    db = client["stock_data"]
    collection = db["icici_bank"]

    # Define the ticker symbol and time window
    ticker = "ICICIBANK.NS"
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)  # Collect data for the past week

    # Fetch data with a 15-minute interval
    icici_data = yf.download(ticker, start=start_time, end=end_time, interval="15m")

    # Store the data in MongoDB
    if not icici_data.empty:
        data_dict = icici_data.to_dict(orient="split")
        data_list = []
        for i in range(len(data_dict["index"])):
            data_item = {
                "timestamp": data_dict["index"][i],
                "open": data_dict["data"][i][0],
                "high": data_dict["data"][i][1],
                "low": data_dict["data"][i][2],
                "close": data_dict["data"][i][3],
                "volume": data_dict["data"][i][4],
            }
            data_list.append(data_item)

        collection.insert_many(data_list)
        print(f"Stored {len(data_list)} records in MongoDB.")

if __name__ == "__main__":
    fetch_and_store_data()
