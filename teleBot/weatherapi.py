import requests, json
from datetime import datetime

# Enter your API key here 
api_key = ""
  
# base_url variable to store url 
base_url = "http://api.openweathermap.org/data/2.5/weather?"


# Openweathermap Weather codes and corressponding emojis
thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis

###
  
def GetWeather(city):

    complete_url = base_url + "q=" + city + "&appid=" + api_key
  
    response = requests.get(complete_url) 
    x = response.json() 

    if x["cod"] != "404": 

        name = x["name"] # city
        
        y = x["main"] 
        current_humidiy = y["humidity"] 
        current_temperature = y["temp"] # in Kelvin
        feels_like = y["feels_like"] # in Kelvin

        # Kelvin = Celsius + 273.15
        # Celsius = Kelvin - 273.15

        current_temperature = "{:.1f}".format(current_temperature - 273.15)
        feels_like = "{:.1f}".format(feels_like - 273.15)

        z = x["weather"] 
        weather_description = z[0]["description"] 

        w = x["wind"] 
        wind_speed = w["speed"] 

        s = x["sys"]
        sunrise = s["sunrise"] # timestamp
        sunset = s["sunset"] # timestamp
        country = s["country"] # timestamp

        sunrise = datetime.fromtimestamp(sunrise) # date and time
        sunset = datetime.fromtimestamp(sunset) # date and time

        stats = [name, country, current_temperature, feels_like, current_humidiy, wind_speed, sunrise, sunset, weather_description]

        return stats
        # print (stats)
        # print(str(stats[0]) + ", " + str(stats[1]) + "\n\n"
        # + "<b>Temperature</b>: " + str(stats[2]) + " C" + "\n"
        # + "<b>Feels like</b>: " + str(stats[3]) + " C" + "\n"
        # + "<b>Humidity</b>: " + str(stats[4]) + " %" + "\n"
        # + "<b>Wind</b>: " + str(stats[5]) + " m/s" + "\n"
        # + "<b>Sunrise</b>: " + str(stats[6])[11:][:5] + "\n"
        # + "<b>Sunset</b>: " + str(stats[7])[11:][:5] + "\n\n"
        # + str(stats[8]).capitalize()) 
    
    else: 
        return "City Not Found"
        
# GetWeather("Newcastle upon Tyne")

# Example Data
# {"coord": { "lon": 139,"lat": 35},
#   "weather": [
#     {
#       "id": 800,
#       "main": "Clear",
#       "description": "clear sky",
#       "icon": "01n"
#     }
#   ],
#   "base": "stations",
#   "main": {
#     "temp": 281.52,
#     "feels_like": 278.99,
#     "temp_min": 280.15,
#     "temp_max": 283.71,
#     "pressure": 1016,
#     "humidity": 93
#   },
#   "wind": {
#     "speed": 0.47,
#     "deg": 107.538
#   },
#   "clouds": {
#     "all": 2
#   },
#   "dt": 1560350192,
#   "sys": {
#     "type": 3,
#     "id": 2019346,
#     "message": 0.0065,
#     "country": "JP",
#     "sunrise": 1560281377,
#     "sunset": 1560333478
#   },
#   "timezone": 32400,
#   "id": 1851632,
#   "name": "Shuzenji",
#   "cod": 200
# }