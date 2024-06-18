import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from datetime import datetime

# Database connection using SQLAlchemy for convenience
engine = create_engine('postgresql://user:password@host/db')

# Function to calculate statistics and insert into the database
def calculate_and_store_stats():
    conn = engine.connect()

    # Load data from the database
    query = """
    SELECT 
        station_id, 
        DATE_PART('year', date) as year, 
        max_temperature, 
        min_temperature, 
        precipitation 
    FROM 
        WeatherData
    """
    df = pd.read_sql(query, conn)

    # Calculate statistics
    stats = df.groupby(['station_id', 'year']).agg(
        avg_max_temp=('max_temperature', lambda x: x[x.notnull()].mean()),
        avg_min_temp=('min_temperature', lambda x: x[x.notnull()].mean()),
        total_precipitation=('precipitation', lambda x: x[x.notnull()].sum() / 10)  # Convert to cm
    ).reset_index()

    # Insert statistics into WeatherStats table
    stats.to_sql('WeatherStats', conn, if_exists='replace', index=False, method='multi')

    conn.close()

# Main function
def main():
    start_time = datetime.now()
    print(f"Calculation and insertion started at {start_time}")

    calculate_and_store_stats()

    end_time = datetime.now()
    print(f"Calculation and insertion finished at {end_time}")
    print(f"Duration: {end_time - start_time}")

if __name__ == "__main__":
    main()
