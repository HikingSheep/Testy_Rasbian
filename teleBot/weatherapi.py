import requests, json

# Enter your API key here 
api_key = ""
  
# base_url variable to store url 
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
def GetWeather(city):

    complete_url = base_url + "q=" + city + "&appid=" + api_key
  
    response = requests.get(complete_url) 
    x = response.json() 

    if x["cod"] != "404": 

        y = x["main"] 
        current_humidiy = y["humidity"] 
        current_temperature = y["temp"] # in Kelvin

        # Kelvin = Celsius + 273.15
        # Celsius = Kelvin - 273.15

        current_temperature = "{:.1f}".format(current_temperature - 273.15)

        z = x["weather"] 
        weather_description = z[0]["description"] 

        w = x["wind"] 
        wind_speed = w["speed"] 

        stats = [current_humidiy, current_temperature, weather_description, wind_speed]

        return stats
    
    else: 
        return "City Not Found"

# GetWeather("Newcastle")
