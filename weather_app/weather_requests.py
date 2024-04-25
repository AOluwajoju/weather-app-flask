import requests
from .models import Weather
from .models import Location
from flask_login import current_user
from . import db

def save_location(longitude, latitude, city, country, id):
    location_temp = Location(longitude=longitude, 
                             latitude=latitude, 
                             city=city,
                             country=country,
                             saved_by_id=id)
    db.session.add(location_temp)
    db.session.commit()


def make_request(param, locationData, error, location):
    # Define the API endpoint URL
    url = f"http://api.weatherapi.com/v1/current.json?key=708c894bf3324951898134601242003&q={param}&aqi=no"
    # Make a GET request to the API
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        try:
            weather = Weather(longitude=data['location']['lon'], 
                              latitude=data['location']['lat'], 
                              city=data['location']['name'],
                              country=data['location']['country'],
                              icon=data['current']['condition']['icon'],
                              temperature=data['current']['temp_c'],
                              condition=data['current']['condition']['text'],
                              queried_by=current_user)
            db.session.add(weather)
            db.session.commit()
            if location == '1':
                
                save_location(data['location']['lon'], 
                              data['location']['lat'], 
                              data['location']['name'], 
                              data['location']['country'], 
                              current_user.id
                              )
            

            locationData.update({
                'longitude': data['location']['lon'],
                'latitude': data['location']['lat'],
                'city': data['location']['name'],
                'country': data['location']['country'],
                'icon': data['current']['condition']['icon'],
                'temperature': data['current']['temp_c'],
                'condition': data['current']['condition']['text']
            })
        except Exception as e:
            print("Error:", e)
    elif response.status_code == 400:
        error = "No matching location found."
    else:
        error = "Something went wrong. Try again."
