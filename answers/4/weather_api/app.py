from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flasgger import Swagger
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_user:password@host/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
swagger = Swagger(app)

from models import WeatherData, WeatherStats, WeatherDataSchema, WeatherStatsSchema

weather_data_schema = WeatherDataSchema(many=True)
weather_stats_schema = WeatherStatsSchema(many=True)

@app.route('/api/weather', methods=['GET'])
def get_weather():
    query = WeatherData.query
    station_id = request.args.get('station_id')
    date = request.args.get('date')

    if station_id:
        query = query.filter(WeatherData.station_id == station_id)
    if date:
        query = query.filter(WeatherData.date == date)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    data = query.paginate(page, per_page, False)

    return jsonify({
        'weather_data': weather_data_schema.dump(data.items),
        'total': data.total,
        'pages': data.pages,
        'page': data.page
    })

@app.route('/api/weather/stats', methods=['GET'])
def get_weather_stats():
    query = WeatherStats.query
    station_id = request.args.get('station_id')
    year = request.args.get('year')

    if station_id:
        query = query.filter(WeatherStats.station_id == station_id)
    if year:
        query = query.filter(WeatherStats.year == year)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    data = query.paginate(page, per_page, False)

    return jsonify({
        'weather_stats': weather_stats_schema.dump(data.items),
        'total': data.total,
        'pages': data.pages,
        'page': data.page
    })

if __name__ == '__main__':
    app.run(debug=True)
