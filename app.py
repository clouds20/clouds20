import requests
import json
from flask import Flask, render_template
from datetime import datetime

#Return icon based on forecast
def weather_icon(forecast):
  if 'fair' in forecast.lower():
     i = 'partly_cloudy_day'
  elif 'thunder' in forecast.lower():
     i = 'thunderstorm'
  elif 'rain' in forecast.lower():
     i = 'rainy'
  elif 'sunny' in forecast.lower():
     i = 'sunny'
  elif 'cloudy' in forecast.lower():
     i= 'cloudy'
  return i

app = Flask(__name__)

@app.route('/')
def index():
    #Retrieve current date
    current_date = datetime.today()
    params = {"datetime": current_date.strftime("%Y-%m-%d[T]%H:%M:%S")} # YYYY-MM-DD

    #Retrieve real time air temperature data from data.gov.sg
    current_data = requests.get('https://api.data.gov.sg/v1/environment/air-temperature',params=params).json()

    #Retrieve current temperature
    current_temp = current_data['items'][0]['readings'][0]['value']

    #Retrieve 24-hour weather forecast data from  data.gov.sg
    data = requests.get('https://api.data.gov.sg/v1/environment/24-hour-weather-forecast').json()

    #Retrieve 24-hour weather forecasts data from JSON array
    today = data['items'][0]

    #Convert date format
    datetimeobj = datetime.strptime(today['timestamp'][0:10],'%Y-%m-%d')
    today['timestamp'] =  datetimeobj.strftime('%A, %d %b %Y')

    #Create a new list for the data
    forecast = [{'date' : today['timestamp'], 'forecast' : today['general']['forecast'], 'temperature': {'high': today['general']['temperature']['high'], 'low': today['general']['temperature']['low']}, 'icon' : weather_icon(today['general']['forecast'])}]

    #Retrieve 4-day weather forecast data from  data.gov.sg
    fourday_data = requests.get('https://api.data.gov.sg/v1/environment/4-day-weather-forecast').json()

    #Retrieve 4-day weather forecasts data from JSON array
    fourday = fourday_data['items'][0]['forecasts']

    #Convert date format 
    for day in fourday:
        datetimeobj = datetime.strptime(day['date'], '%Y-%m-%d')
        day['date'] = datetimeobj.strftime('%A, %d %b %Y')
        #Add four-day forecsst to the new list
        forecast.append({'date' : day['date'], 'forecast' : day['forecast'], 'temperature': {'high': day['temperature']['high'], 'low': day['temperature']['low']}, 'icon' : weather_icon(day['forecast'])})

    return render_template('index.html', current_temp=current_temp, forecast=forecast)

if __name__ == '__main__':
    app.run()

