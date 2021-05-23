#import and setup
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

#import flask
from flask import Flask, jsonify

#sqlalchemy connection
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# create an app, b
app = Flask(__name__)

#list all routes
#Welcome page - Home page
@app.route('/')
def welcome():
    return(
        f"Welcome to Honolulu, Hawaii Climate Analysis<br/>"
        f"Below are available routes:<br/>"
        f"<br/>"
        f"Precipitation Data<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"Percipitation Station Information<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"Temperature Observation (Year from Last Data Point)<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"Minimum, Maximum, and Average Temperature from a given start date <br/>"
        f"/api/v1.0/yyyymmdd<br/>"
        f"<br/>"
        f"Minimum, Maximum, and Average Temperature from a given start-end date range<br/>"
        f"/api/v1.0/yyyymmdd/yyyymmdd"  
    )

#Precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Dates and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).all()
    prcp_date = dict(results)

    #jsonify result
    return jsonify(prcp_date)

    
#Stations
@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    #All stations
    station = session.query(Station.name).all()
    station_list = list(np.ravel(station))
    #jsonify result
    return jsonify(station_list)


#Temperature Observations
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    #recent date + date from one year ago
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = (dt.datetime.strptime(recent_date[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')
    
    #tobs
    tobs_result = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > one_year_ago).all()
    #make list
    tobs_list = list(np.ravel(tobs_result))
    
    #jsonify
    return jsonify(tobs_list)


    
#Temps by Start Date
#min, max, avg temp
@app.route('/api/v1.0/<start>')
def temp_start(start):    
#     start = dt.datetime.strptime(start, '%Y%m%d')
    
    session = Session(engine)
#     date1 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start).all()

#     temp_start = list(np.ravel(date1))
    
#     return jsonify(temp_start)
    

    #trial and error
    #start time
    start_date = dt.datetime.strptime(start, '%Y%m%d')
#     one_year_ago2 = date1 - dt.timedelta(days=365)
   
    #min, max, avg temp
    
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > start_date).all()
    high_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > start_date).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > start_date).all()

    #jsonify
    
    return jsonify(f"Date:{start_date} : Minimum Temperature: {low_temp}, Maximum Temperature: {high_temp}, Average Temperature: {avg_temp}")
    

#Temps by Start-End Date
@app.route('/api/v1.0/<start>/<end>')
def temp_start_end(start,end):
#     start2 = dt.datetime.strptime(start,'%Y%m%d')
#     end2 = dt.datetime.strptime(end,'%Y%m%d')
    
    session = Session(engine)
#     date2 = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date > start2).filter(Measurement.date < end2).all()
    
#     temp_start_end = list(np.ravel(date2))
    
#     return jsonify(temp_start_end)
    
#trial and error


    #start and end date
    date1 = dt.datetime.strptime(start, '%Y%m%d')
    date2 = dt.datetime.strptime(end, '%Y%m%d')
    #min, max, avg temp
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > date1).filter(Measurement.date < date2).all()
    high_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > date1).filter(Measurement.date < date2).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > date1).filter(Measurement.date < date2).all()

    #jsonify
    return jsonify(f"Date: {date1} to {date2}, Minimum Temperature: {low_temp}, Maximum Temperature: {high_temp}, Average Temperature: {avg_temp}")
                            
                            
if __name__ == "__main__":
    app.run(debug=True)