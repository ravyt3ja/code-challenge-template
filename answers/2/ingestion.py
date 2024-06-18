import os
import pandas as pd
import psycopg2
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(filename='ingestion.log', level=logging.INFO, 
                    format='%(asctime)s %(message)s')

# Function to handle missing values
def handle_missing_values(value):
    return None if value == -9999 else value

# Connect to PostgreSQL database
def get_db_connection():
    return psycopg2.connect(
        dbname="db", 
        user="user", 
        password="password", 
        host="host"
    )

def ingest_data(file_path, station_id):
    # Load data from file
    df = pd.read_csv(file_path, delimiter='\t', header=None, 
                     names=['date', 'max_temp', 'min_temp', 'precipitation'])
    
    # Handle missing values
    df['max_temp'] = df['max_temp'].apply(handle_missing_values)
    df['min_temp'] = df['min_temp'].apply(handle_missing_values)
    df['precipitation'] = df['precipitation'].apply(handle_missing_values)
    
    # Convert date to datetime format
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    
    # Insert data into the database
    conn = get_db_connection()
    cur = conn.cursor()
    
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO WeatherData (station_id, date, max_temperature, min_temperature, precipitation)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (station_id, date) DO NOTHING
        """, (station_id, row['date'], row['max_temp'], row['min_temp'], row['precipitation']))
    
    conn.commit()
    cur.close()
    conn.close()
    return len(df)

def main():
    start_time = datetime.now()
    logging.info("Ingestion started")

    wx_data_dir = '/Users/raviteja/Documents/code-challenge-template/wx_data'
    total_records = 0
    
    for file_name in os.listdir(wx_data_dir):
        if file_name.endswith('.txt'):
            file_path = os.path.join(wx_data_dir, file_name)
            station_id = os.path.splitext(file_name)[0]
            records_ingested = ingest_data(file_path, station_id)
            total_records += records_ingested
            logging.info(f"Ingested {records_ingested} records from {file_name}")
    
    end_time = datetime.now()
    logging.info(f"Ingestion finished: {total_records} records ingested")
    logging.info(f"Duration: {end_time - start_time}")

if __name__ == "__main__":
    main()
