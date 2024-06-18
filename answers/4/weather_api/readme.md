# Weather API

## Setup

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Set up PostgreSQL database and update connection details in `app.py`.

3. Run the application:
    ```bash
    python app.py
    ```

4. Access the Swagger documentation at `http://localhost:5000/apidocs`.

## Endpoints

- `/api/weather`: Get weather data. Supports filtering by `station_id` and `date`. Supports pagination with `page` and `per_page` query parameters.
- `/api/weather/stats`: Get weather statistics. Supports filtering by `station_id` and `year`. Supports pagination with `page` and `per_page` query parameters.
