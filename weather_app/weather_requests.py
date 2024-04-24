import requests

def make_request(param, locationData, error, g, db, location):
    # Define the API endpoint URL
    url = f"http://api.weatherapi.com/v1/current.json?key=708c894bf3324951898134601242003&q={param}&aqi=no"
    # Make a GET request to the API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        try:
            db.execute(
                "INSERT INTO weather (longitude, latitude, city, country, icon, temperature, condition, queried_by) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (data['location']['lon'],
                 data['location']['lat'],
                 data['location']['name'],
                 data['location']['country'],
                 data['current']['condition']['icon'],
                 data['current']['temp_c'],
                 data['current']['condition']['text'],
                 g.user['id']),
            )

            if location == '1':
                db.execute(
                    "INSERT OR IGNORE INTO locations (longitude, latitude, city, country, saved_by) VALUES (?, ?, ?, ?, ?)",
                    (data['location']['lon'],
                     data['location']['lat'],
                     data['location']['name'],
                     data['location']['country'],
                     g.user['id']),
                )
            db.commit()

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
