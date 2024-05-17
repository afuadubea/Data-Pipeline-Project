# BTC-USA Data Pipeline Project (ETL)

## Overview

This project is an ETL (Extract, Transform, Load) data pipeline that handles real-time data collection, ingestion, storage, and visualization. The pipeline is designed to collect data from a source, ingest it using Python, store it in a data lake on AWS S3, and load it into an AWS Redshift data warehouse. Finally, the data is retrieved for analysis and visualization using Power BI.

## Project Structure

- **Source Data**: Real-time data collection from data source.
- **Ingestion**: Data ingested using Python scripts.
- **Data Lake**: Persisting ingested data as a zip file in AWS S3.
- **Data Warehouse**: Loading data from AWS S3 into AWS Redshift.
- **Visualization**: Analyzing and visualizing data with Power BI.

## Steps

### Data Collection
- Real-time data is collected from the source.
- Source Link: [https://finance.yahoo.com/]

### Data Ingestion
- Python scripts are used to ingest the collected data.
- The data is processed and transformed as required.

### Data Storage
- The transformed data is stored as a zip file in AWS S3.
- This serves as a data lake for persistent storage.

### Data Loading
- The stored data from AWS S3 is loaded into AWS Redshift.
- Redshift acts as the data warehouse for efficient querying and analysis.

### Data Visualization
- Data is retrieved from AWS Redshift.
- Power BI is used to create visualizations and dashboards for data analysis.

## Prerequisites

- AWS Account
- AWS S3 Bucket
- AWS Redshift Cluster
- Power BI
- Python 3.x
- Required Python Libraries: boto3, pandas etc.

### Contributing
- Contributions are welcome! Please fork the repository and create a pull request.

### License
-This project is licensed under the MIT License.

