# Example of handling missing values in Python before inserting into the database
import pandas as pd
import psycopg2

# Function to handle missing values and convert them to None
def handle_missing_values(value):
    return None if value == -9999 else value

# Load data from a file
df = pd.read_csv('wx_data/station1.txt', delimiter='\t', header=None, names=['date', 'max_temp', 'min_temp', 'precipitation'])

# Apply the function to handle missing values
df['max_temp'] = df['max_temp'].apply(handle_missing_values)
df['min_temp'] = df['min_temp'].apply(handle_missing_values)
df['precipitation'] = df['precipitation'].apply(handle_missing_values)

# Connect to PostgreSQL database and insert data
conn = psycopg2.connect(dbname="db", user="user", password="password", host="host")
cur = conn.cursor()

for index, row in df.iterrows():
    cur.execute("""
        INSERT INTO WeatherData (station_id, date, max_temperature, min_temperature, precipitation)
        VALUES (%s, %s, %s, %s, %s)
    """, ('station1', row['date'], row['max_temp'], row['min_temp'], row['precipitation']))

conn.commit()
cur.close()
conn.close()
