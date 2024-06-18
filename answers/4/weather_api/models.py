from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

class WeatherData(db.Model):
    __tablename__ = 'WeatherData'
    station_id = db.Column(db.String(50), primary_key=True)
    date = db.Column(db.Date, primary_key=True)
    max_temperature = db.Column(db.Integer)
    min_temperature = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)

class WeatherStats(db.Model):
    __tablename__ = 'WeatherStats'
    station_id = db.Column(db.String(50), primary_key=True)
    year = db.Column(db.Integer, primary_key=True)
    avg_max_temp = db.Column(db.Float)
    avg_min_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)

class WeatherDataSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherData

class WeatherStatsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WeatherStats
