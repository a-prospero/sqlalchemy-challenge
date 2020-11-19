import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Query for the dates and precipitation values from the last year.
# Convert the query results to a Dictionary using date as the key and tobs as the value.
# Return the json representation of your dictionary.
@app.route("/")
def home_page():
    return(
        f"Welcome to my Home Page <br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs <br>"
        f"/api/v1.0/start <br>"
        f"/api/v1.0/<start>/<end> <br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Return a list of measurement date and prcp information from the last year """
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    precipitation_values = [results]
#Create dictionary
    # for p in results:
    #     prcp_dict = {}
    #     prcp_dict["date"] = p.date  
    #     prcp_dict["precipitation"] = p.prcp
    #     precipitation_values.append(prcp_dict)

    return jsonify(precipitation_values)

@app.route("/api/v1.0/stations")
def stations():
    """ Return a JSON list of stations from the dataset."""
    station_results = session.query(Station)
    station_values = []
#Create dictionary
    for s in station_results:
        station_dict = {}
        station_dict["name"] = s.name 
        station_dict["station"] = s.station
        station_values.append(station_dict)

    return jsonify(station_values)


@app.route("/api/v1.0/tobs")
def temp():
    """ Query the dates and temperature observations of the most active station for the last year of data.."""
    #most_active_station = session.query(Measurement.station, func.count(Measurement.tobs)).\
    filter(Measurement.station == Station.station).group_by(Measurement.station).order_by(func.count(Measurement.tobs).desc()).all()
    tobs_station = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >="2016-08-23").\
    filter(Measurement.station == "USC00519281")
    tobs_values = []
#Create dictionary
    for temp in tobs_station:
        tobs_dict = {}
        tobs_dict["station"] = temp.station 
        tobs_dict["temperature"] = temp.tobs
        tobs_values.append(tobs_dict)

    return jsonify(tobs_values)

@app.route('/api/v1.0/start')
def get_t_start(start):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()

    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

app.route("/api/v1.0/yyyy-mm-dd/")
def get_t_start_stop(start,stop):
    session = Session(engine)
    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= stop).all()
    session.close()

    tobsall = []
    for min,avg,max in queryresult:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobsall.append(tobs_dict)

    return jsonify(tobsall)



if __name__ == '__main__':
    app.run(debug=True)

# Return a json list of stations from the dataset