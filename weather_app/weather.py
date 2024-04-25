from datetime import datetime, timedelta


from flask import (
    Blueprint, flash, render_template, request, redirect, url_for
)

from . import db

from .models import Weather
from .models import Location

from weather_app.auth import login_required

from weather_app.weather_requests import make_request, save_location

from flask_login import login_required, current_user

bp = Blueprint('weather', __name__, url_prefix='/weather')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def weather():        
    locationData = {}        
    locations = [] 
    
    def get_locations():
        nonlocal locations
        
        locations =  Location.query.filter_by(saved_by_id=current_user.id).all()
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
                    result = Weather.query.filter_by(latitude=round(float(coords[0]), 2), longitude=round(float(coords[1]), 2)).first()
                    
                    if result:
                        timestamp = result.date_accessed
                        
                        # Check if the timestamp is older than 24 hours
                        if timestamp < (datetime.now() - timedelta(hours=24)):
                            db.session.delete(result)
                            
                            location_temp= Location.query.filter_by(latitude=result.latitude, longitude=result.longitude).first()
                            db.session.delete(location_temp)
                            
                            db.session.commit()

                            make_request(value, locationData, error, location)                        
                        else:
                            #use result
                            get_locations()
                            
                            if location=="1":
                                #if location is not saved
                                location_temp =  Location.query.filter_by(latitude=result.latitude, longitude=result.longitude).first()
                                if location_temp is None:
                                    save_location(result.longitude, result.latitude, result.city, result.country, current_user.id)
                            
                            return render_template('weather.html', data=result, locations=locations)
                    else:

                        make_request(value, locationData, error, location)
                    
            elif parameter == 'city':
                value = value.strip() #remove trailing spaces
                # check if record with coordinates exists
                result = Weather.query.filter_by(city=value[0].upper() + value[1:]).first()
                print(result)
                
                if result is not None:
                    timestamp = result.date_accessed
                    
                    # Check if the timestamp is older than 24 hours
                    if timestamp < (datetime.now() - timedelta(hours=24)):
                        weather_temp= Weather.query.filter_by(city=value.strip()).first()
                        db.session.delete(weather_temp)
                        db.session.commit()

                        make_request(value, locationData, error, location)                        
                    else:
                        #use result
                        get_locations()
                        
                        if location=="1":
                                #if location is not saved
                                location_temp =  Location.query.filter_by(latitude=result.latitude, longitude=result.longitude).first()
                                if location_temp is None:
                                    save_location(result.longitude, result.latitude, result.city, result.country, current_user.id)
                                    
                        return render_template('weather.html', data=result, locations=locations)
                else:

                    make_request(value, locationData, error, location)
                    
                    
        flash(error)
    get_locations()
    return render_template('weather.html', data=locationData, locations=locations)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    location_temp= Location.query.get_or_404(id)
    db.session.delete(location_temp)
    db.session.commit()
    return redirect(url_for('weather.weather'))