from datetime import datetime, timedelta


from flask import (
    Blueprint, flash, g, render_template, request, redirect, url_for
)

from weather_app.db import get_db
from weather_app.auth import login_required

from weather_app.weather_requests import make_request



bp = Blueprint('weather', __name__, url_prefix='/weather')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def weather():        
    locationData = {}        
    db = get_db()
    locations = [] 
    
    def get_locations():
        nonlocal locations
        
        locations =  db.execute(
            "SELECT * FROM locations WHERE saved_by = ?",
            (g.user['id'],),
        ).fetchall()
    
    get_locations()

    if request.method == 'POST':
        parameter = request.form['parameter']
        value = request.form['value']
        location = request.form['location']
        error = None    
        

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
                            db.execute("DELETE FROM locations WHERE latitude = ? AND longitude = ?", (
                                round(float(coords[0]), 2), 
                                round(float(coords[1]), 2),
                                ))
                            
                            db.commit()

                            make_request(value, locationData, error, g, db, location)                        
                        else:
                            #use result
                            get_locations()
                            return render_template('weather.html', data=result, locations=locations)
                    else:

                        make_request(value, locationData, error, g, db, location)
                    
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

                        make_request(value, locationData, error, g, db, location)                        
                    else:
                        #use result
                        get_locations()
                        return render_template('weather.html', data=result, locations=locations)
                else:

                    make_request(value, locationData, error, g, db, location)
                    
                    
        flash(error)
    get_locations()
    return render_template('weather.html', data=locationData, locations=locations)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM locations WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('weather.weather'))