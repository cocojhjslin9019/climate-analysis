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
        f"Minimum, Maximum, and Average Temperature from a given start date (yyyy-mm-dd)<br/>"
        f"/api/v1.0/<start><br/>"
        f"<br/>"
        f"Minimum, Maximum, and Average Temperature from a given start-end date range (yyyy-mm-dd/yyyy-mm-dd)<br/>"
        f"/api/v1.0/<start><end>"  
    )

#Precipitation
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Dates and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    prcp_date = dict(results)

    #jsonify result
    return jsonify(prcp_date)

    
#Stations
@app.route('/api/v1.0/stations')
def stations():
    #All stations
    new_station = session.query(func.distinct(Station.station).all()
    #jsonify result
    return jsonify(new_station)


#Temperature Observations
@app.route('/api/v1.0/tobs')
def tobs():
   
    #get last date from year ago
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)              
                                
    #date and temperature
    this_station = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date > one_year_ago).filter(Measurement.station == 'USC00519281').all()
    station_list = list(this_station)
    
    #jsonify
    return jsonify(station_list)


    
#Temps by Start Date
#min, max, avg temp
@app.route('/api/v1.0/<start>')
def temp_start(start):
    #start time
    date1 = dt.datetime.strptime(start, '%Y-%m-%d')
    one_year_ago2 = date1 - dt.timedelta(days=365)
    #min, max, avg temp
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > one_year_ago2).all()
    high_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > one_year_ago2).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > one_year_ago2).all()

    #jsonify
    return jsonify(f"Date:{date1} : Minimum Temperature: {low_temp}, Maximum Temperature: {high_temp}, Average Temperature: {avg_temp}")
    

#Temps by Start-End Date
@app.route('/api/v1.0/<start><end>')
def temp_start_end():
    #start and end date
    date1 = dt.datetime.strptime(start, '%Y-%m-%d')
    date2 = dt.datetime.strptime(end, '%Y-%m-%d')
    #min, max, avg temp
    low_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date > date1).filter(Measurement.date < date2).all()
    high_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date > date1).filter(Measurement.date < date2).all()
    avg_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.date > date1).filter(Measurement.date < date2).all()

    #jsonify
    return jsonify(f"Date: {date1} to {date2}, Minimum Temperature: {low_temp}, Maximum Temperature: {high_temp}, Average Temperature: {avg_temp}")
                            
                            
if __name__ == "__main__":
    app.run(debug=True)