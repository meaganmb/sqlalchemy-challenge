import numpy as np
import datetime as dt

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
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"input start and end date as yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    year_ago = dt.date(2017, 8 ,23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    date_list = list(np.ravel(results))

    return jsonify(date_list)


@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    result = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(result))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    year_ago = dt.date(2017, 8 ,18) - dt.timedelta(days=365)
    
    result = session.query(Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= year_ago).\
                    filter(Measurement.station == "USC00519281").all()

    session.close()

    # Convert list of tuples into normal list
    most_active = list(np.ravel(result))

    return jsonify(most_active)


@app.route("/api/v1.0/<start>")
def date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    result = session.query(func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).all()

    session.close()

    # Convert list of tuples into normal list
    start_json = list(np.ravel(result))

    return jsonify(start_json)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query
    result = session.query(func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start).\
            filter(end >= Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    start_end_json = list(np.ravel(result))

    return jsonify(start_end_json)


if __name__ == '__main__':
    app.run(debug=True)