import numpy as np

import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# This function called `calc_temps` will accept start date and end date in the format '%Y-%m-%d' 
# and return the minimum, average, and maximum temperatures for that range of dates
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    session = Session(engine)

    return session.query(Measurement.station, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/&#60;start&#62; <br/>"
        f"/api/v1.0/&#60;start&#62;/&#60;end> <br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query
    session = Session(engine)
    prcp_results = session.query(Measurement.date, func.sum(Measurement.prcp)).group_by(Measurement.date).all()
    
    all_prcp_by_date = [{i[0]: i[1]} for i in prcp_results]

    return jsonify(all_prcp_by_date)


#/api/v1.0/stations
#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    # Query
    session = Session(engine)
    station_results = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).order_by(Station.station).all()
    
    all_stations = {}

    for station, name, latitude, longitude, elevation in station_results:
        all_stations[station] = {"name": name}
        all_stations[station]["latitude"] = latitude
        all_stations[station]["longitude"] = longitude
        all_stations[station]["elevation"] = elevation

    return jsonify(all_stations)

#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    # Query
    session = Session(engine)
    
    where_end_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    where_start_date = (dt.datetime.strptime(where_end_date, '%Y-%m-%d') - dt.timedelta(days=365)).date()
    
    tobs_results = engine.execute(f"SELECT date, prcp FROM measurement Where date >= '{where_start_date}' and date < '{where_end_date}' and prcp IS NOT NULL").fetchall()
    
    all_tobs_results = [{i[0]: i[1]} for i in tobs_results]

    return jsonify(all_tobs_results)

@app.route("/api/v1.0/<start_date>")
def by_start_date(start_date): 
    
    by_start_date_results = engine.execute(f"SELECT Station, MIN(tobs) as 'Minimum Temp', max(tobs) as 'Maximum Temp', avg(tobs) as 'Average Temp' \
                                        FROM measurement m \
                                        WHERE date >= '{start_date}'").fetchall()
      
    #all_by_start_date_results = [{i[0]: i[1]} for i in by_start_date_results]
    all_by_start_date_results = {}
    
    for station, minimum, maximum, average in by_start_date_results:
        all_by_start_date_results[station] = {"station":station}
        all_by_start_date_results[station]["minimum"] = minimum
        all_by_start_date_results[station]["maximum"] = maximum
        all_by_start_date_results[station]["average"] = average
        all_by_start_date_results[station]["date"] = start_date

    return jsonify(all_by_start_date_results)


@app.route("/api/v1.0/<start_date>/<end_date>")
def between_dates(start_date, end_date): 
    
    between_dates_results = calc_temps(start_date, end_date)
    
    all_between_dates_results = {}
    
    for station, minimum, maximum, average in between_dates_results:
        all_between_dates_results[station] = {"station":station}
        all_between_dates_results[station]["minimum"] = minimum
        all_between_dates_results[station]["maximum"] = maximum
        all_between_dates_results[station]["average"] = average
        all_between_dates_results[station]["start_date"] = start_date
        all_between_dates_results[station]["end_date"] = end_date

    return jsonify(all_between_dates_results)    



if __name__ == '__main__':
    app.run(debug=True)