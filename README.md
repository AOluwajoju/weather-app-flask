# weather-app-flask

# Local Setup

To setup this project.

- Clone this github repo or download and extract the resulting zip folder in your local machine/server.
- Activate the python virtual environment in the project directory. You can do so using the following code in python3

  `$ .venv\scripts\activate`

- cd into the folder and install the dependencies in requirements.txt (just in case)

  `(venv)$ pip3 install -r requirements.txt`

  To setup Database.

- activate the python shell by running

  `python`
  or
  `python3` (for python 3)

- once the shell is activated, run the following code in order

  `>>> from weather_app import db, create_app`
  `>>> app=create_app()`
  `>>> with app.app_context():`
  `...        db.create_all()`

- close the shell

  `>>> exit()`

  To start the server

- in the virtual environment, run:

  `flask --app weather_app run --debug`
