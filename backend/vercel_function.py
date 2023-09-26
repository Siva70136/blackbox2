from fetch_data import fetch_and_store_data

# Trigger the data retrieval process when this serverless function is called
def main(request):
    fetch_and_store_data()
    return {"message": "Data retrieval process started."}
