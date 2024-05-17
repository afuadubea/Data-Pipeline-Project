import boto3
import zipfile
import io
import pandas as pd
import psycopg2
from io import StringIO

def ingest_csv_to_redshift(s3_bucket, s3_zip_file, redshift_table, redshift_db, redshift_user, redshift_password, redshift_host, redshift_port):
    # Initialize S3 client
    s3 = boto3.client('s3')

    # Download the zip file from S3
    zip_obj = s3.get_object(Bucket=s3_bucket, Key=s3_zip_file)
    buffer = io.BytesIO(zip_obj['Body'].read())

    # Unzip the file in memory
    with zipfile.ZipFile(buffer, 'r') as z:
        # Assuming there's only one file in the zip
        csv_filename = z.namelist()[0]
        with z.open(csv_filename) as f:
            df = pd.read_csv(f)
    
    # Convert DataFrame to CSV in memory
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Connect to Redshift
    conn = psycopg2.connect(
        dbname=redshift_db,
        user=redshift_user,
        password=redshift_password,
        host=redshift_host,
        port=redshift_port
    )
    cursor = conn.cursor()

    # Create table if it doesn't exist (You need to define the table schema)
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {redshift_table} (
        -- Define your table schema here
        column1_name column1_type,
        column2_name column2_type,
        ...
    );
    """)

    # Use the COPY command to load data from S3
    cursor.copy_expert(f"COPY {redshift_table} FROM STDIN WITH CSV HEADER DELIMITER ',' NULL AS 'NULL' TIMEFORMAT 'auto' ACCEPTINVCHARS;", csv_buffer)

    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

# Define your parameters
s3_bucket = "your-s3-bucket"
s3_zip_file = "path/to/your.zip"
redshift_table = "your_redshift_table"
redshift_db = "your_redshift_db"
redshift_user = "your_redshift_user"
redshift_password = "your_redshift_password"
redshift_host = "your_redshift_host"
redshift_port = 5439  # Default Redshift port

# Run the function
ingest_csv_to_redshift(s3_bucket, s3_zip_file, redshift_table, redshift_db, redshift_user, redshift_password, redshift_host, redshift_port)
