import yfinance as yf
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from pymongo import MongoClient
from datetime import datetime, timedelta

# Configure MongoDB
client = MongoClient("mongodb+srv://siva:L7vTobLaY5ndDoaY@cluster0.6nug7fa.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection URL
db = client["stock_data"]
collection = db["icici_bank"]

# Create a scheduler
scheduler = BackgroundScheduler()

def fetch_and_store_data():
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

# Schedule the job to run every 15 minutes from 11:15 AM to 2:15 PM
scheduler.add_job(fetch_and_store_data, "cron", hour="11-14", minute="15", second="0")

# Start the scheduler
scheduler.start()
fetch_and_store_data()

try:
    # Keep the program running
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    # Shut down the scheduler gracefully on program exit
    scheduler.shutdown()
