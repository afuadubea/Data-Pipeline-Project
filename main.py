import time 
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import boto3
import zipfile
import io

# Initialize S3 client
session = boto3.Session("************", "************")
s3 = session.client('s3')

# Specify your bucket name and file name
bucket_name = "bucket_name"
zip_file_name = "zip_filename"

ticker = 'BTC-USD'
period1 = datetime.datetime(2024, 1, 1)
period2 = period1 + relativedelta(days=+152)
interval = '1d'

# Function to upload data to S3
def upload_to_s3(data):
    # Create or open the zip file in memory
    in_memory_zip = io.BytesIO()
    with zipfile.ZipFile(in_memory_zip, mode="a", compression=zipfile.ZIP_DEFLATED) as zf:
        # Add the data to the zip file
        zf.write(data)

    # Reset the position to the beginning to read the BytesIO object
    in_memory_zip.seek(0)

    # Upload the zip file to S3 directly from BytesIO object
    s3.upload_fileobj(in_memory_zip, bucket_name, zip_file_name)

# Load existing data from the CSV file
try:
    existing_data = pd.read_csv('btc_data.csv')
except FileNotFoundError:
    existing_data = pd.DataFrame()

# Loop until the current date reaches the end date
while datetime.datetime.now() < period2:
    # Construct query string with current timestamps
    query_string = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={int(time.mktime(period1.timetuple()))}&period2={int(time.mktime(datetime.datetime.now().timetuple()))}&interval={interval}&events=history&includeAdjustedClose=true'

    # Fetch data for the current date
    data = pd.read_csv(query_string)
    
    # Filter out existing rows from the fetched data
    new_data = data[~data.index.isin(existing_data.index)]
    
    if not new_data.empty:
        # Append the new data to the CSV file
        new_data.to_csv('btc_data.csv', mode='a', header=True, index=False)
        
        # Upload the new data to S3
        upload_to_s3('btc_data.csv')
        
        # Update existing_data with the new data
        existing_data = pd.concat([existing_data, new_data], ignore_index=True)
    
        # Print the current date and time of data fetch
        print(f"Fetched data until {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Move to the next day
    period1 += datetime.timedelta(days=1)
    
    # Wait for one day before fetching data for the next day
    time.sleep(86400)  # 86400 seconds = 1 day

print(data)
