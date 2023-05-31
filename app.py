import requests
import json
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    #Retrieve 24-hour weather forecast data from  data.gov.sg
    data = requests.get('https://api.data.gov.sg/v1/environment/24-hour-weather-forecast').json()

    #Retrieve 24-hour weather forecasts data from JSON array
    today = data['items'][0]

    #Convert date format
    datetimeobj = datetime.strptime(today['timestamp'][0:10],'%Y-%m-%d')
    today['timestamp'] =  datetimeobj.strftime('%A, %d %b %Y')

    #Retrieve 4-day weather forecast data from  data.gov.sg
    fourday_data = requests.get('https://api.data.gov.sg/v1/environment/4-day-weather-forecast').json()

    #Retrieve 4-day weather forecasts data from JSON array
    fourday = fourday_data['items'][0]['forecasts']

    #Convert date format
    for day in fourday:
        datetimeobj = datetime.strptime(day['date'], '%Y-%m-%d')
        day['date'] = datetimeobj.strftime('%A, %d %b %Y')

    return render_template('index.html', today=today, fourday=fourday)

if __name__ == '__main__':
    app.run()

