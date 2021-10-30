import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
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
def home():
    return (
        f"Welcome home!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-02-01"
    )


@app.route("/api/v1.0/precipitation")
def preciptation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Perform a query to retrieve the data and precipitation scores
    year_ago = '2016-08-23'
    last_year_prcp = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date > year_ago).order_by(Measurement.date).all()
   

    session.close()


    # Create a dictionary 
    prcp_list = []
    for date, prcp in last_year_prcp:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations_yo():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Perform a query to retrieve the stations

    stations = session.query(Measurement.station, Station.name).filter(Measurement.station == Station.station).group_by(Station.name).order_by(Measurement.station).all()
    

    session.close()


   
    station_list = []
    for id, name in stations:
        stations_dict = {}
        stations_dict["id"] = id
        stations_dict["name"] = name
        station_list.append(stations_dict)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def temps_waihee():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Perform a query to retrieve the data and temperature observed
    year_ago = '2016-08-23'
    waihee_temp_recent = session.query(Measurement.date,Measurement.tobs).filter(Measurement.station == Station.station).filter(Measurement.station == "USC00519281").filter(Measurement.date > year_ago).order_by(Measurement.date).all()

    session.close()


    # Create a dictionary 
    waihee_list = []
    for date, tobs in waihee_temp_recent:
        waihee_dict = {}
        waihee_dict["date"] = date
        waihee_dict["tobs"] = tobs
        waihee_list.append(waihee_dict)

    return jsonify(waihee_list)



@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    start_str = str(start)
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station == Station.station).filter(Measurement.date >= start_str).order_by(Measurement.date).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == Station.station).filter(Measurement.date >= start_str).order_by(Measurement.date).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station == Station.station).filter(Measurement.date >= start_str).order_by(Measurement.date).all()   
    session.close()


    # Create a dictionary
    temp_list = []

    temp_dict = {}
    temp_dict["low_temp"] = low_temp[0][0]
    temp_dict["avg_temp"] = round(avg_temp[0][0],1)
    temp_dict["max_temp"] = max_temp[0][0]

    temp_list.append(temp_dict)

    return jsonify(temp_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    start_str = str(start)
    end_str = str(end)
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station == Station.station).filter(Measurement.date >= start_str).filter(Measurement.date <= end_str).order_by(Measurement.date).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == Station.station).filter(Measurement.date >= start_str).filter(Measurement.date <= end_str).order_by(Measurement.date).all()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station == Station.station).filter(Measurement.date >= start_str).filter(Measurement.date <= end_str).order_by(Measurement.date).all()   
    session.close()


    # Create a dictionary
    temp_se_list = []

    temp_se_dict = {}
    temp_se_dict["low_temp"] = low_temp[0][0]
    temp_se_dict["avg_temp"] = round(avg_temp[0][0],1)
    temp_se_dict["max_temp"] = max_temp[0][0]

    temp_se_list.append(temp_se_dict)

    return jsonify(temp_se_list)








if __name__ == "__main__":
    app.run(debug=True)
