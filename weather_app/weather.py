import requests
from datetime import datetime, timedelta


from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from weather_app.db import get_db

bp = Blueprint('weather', __name__, url_prefix='/weather')


@bp.route('/', methods=('GET', 'POST'))
def weather():        
    locationData = {}        
    db = get_db()

    if request.method == 'POST':
        parameter = request.form['parameter']
        value = request.form['value']
        error = None
        
        def make_request(param):
            nonlocal error
            nonlocal locationData
            # Define the API endpoint URL
            url = f"http://api.weatherapi.com/v1/current.json?key=708c894bf3324951898134601242003&q={param}&aqi=no"                       
            # Make a GET request to the API
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()
                try:
                    db.execute(
                        "INSERT INTO weather (longitude, latitude, city, country, icon, temperature, condition) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (data['location']['lon'], 
                        data['location']['lat'], 
                        data['location']['name'], 
                        data['location']['country'], 
                        data['current']['condition']['icon'], 
                        data['current']['temp_c'], 
                        data['current']['condition']['text']),
                    )
                    db.commit()
                except Exception as e:
                    print("Error:", e)
                    
                locationData.update({
                    'longitude': data['location']['lon'], 
                    'latitude' : data['location']['lat'],
                    'city' : data['location']['name'], 
                    'country' : data['location']['country'], 
                    'icon' :  data['current']['condition']['icon'], 
                    'temperature' : data['current']['temp_c'], 
                    'condition' : data['current']['condition']['text']
                })
            elif response.status_code == 400:
                error="No matching location found." 
            else:
                error="Something went wrong. Try again."     
        

        if not parameter:
            error = 'Specify the kind of parameter you\'re entering.'
        elif not value:
            error = 'Enter a search value.'

        if error is None:
            # if paremeter is latitude and longitude (coordinates)
            if parameter == 'coords':
                value=value.replace(" ", "") #remove spaces
                coords = value.split(',')
                if len(coords)!=2:
                    error="Invalid format used"
                else:
                
                    # check if record with coordinates exists
                    result = db.execute(
                        "SELECT * FROM weather WHERE latitude = ? AND longitude = ?",
                        (
                            round(float(coords[0]), 2), 
                            round(float(coords[1]), 2),
                        ),
                    ).fetchone()
                    
                    if result:
                        timestamp = result["date_accessed"]
                        
                        # Check if the timestamp is older than 24 hours
                        if timestamp < (datetime.now() - timedelta(hours=24)):
                            db.execute("DELETE FROM weather WHERE latitude = ? AND longitude = ?", (
                                round(float(coords[0]), 2), 
                                round(float(coords[1]), 2),
                                ))
                            db.commit()

                            make_request(value)                        
                        else:
                            #use result
                            return render_template('weather.html', data=result)
                    else:

                        make_request(value)
                    
            elif parameter == 'city':
                value = value.strip() #remove trailing spaces
                # check if record with coordinates exists
                result = db.execute(
                    "SELECT * FROM weather WHERE city = ?",
                    (value[0].upper() + value[1:],),
                ).fetchone()
                
                if result:
                    timestamp = result["date_accessed"]
                    
                    # Check if the timestamp is older than 24 hours
                    if timestamp < (datetime.now() - timedelta(hours=24)):
                        db.execute("DELETE FROM weather WHERE city = ?",
                            (value.strip(),),)
                        db.commit()

                        make_request(value)                        
                    else:
                        #use result
                        return render_template('weather.html', data=result)
                else:

                    make_request(value)
                    
                    
        flash(error)

    return render_template('weather.html', data=locationData)