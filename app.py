from crypt import methods
import requests
from flask import Flask, render_template,request
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html.j2')
def get_health_measures(aqi):
    if 0 <= aqi <= 50:
            return """AQI Level: GOOD<br><br>
        Recommended Measures: <br>Air quality is considered satisfactory, and air pollution poses little or no risk. <br><br>
        Potential Health Impacts: <br>You can breathe deeply and engage in strenuous outdoor exercise without any anticipated health issues.""","green"
    elif 51 <= aqi <= 100:
        return """AQI Level: MODERATE<br><br>
        Recommended Measures: <br>Unusually sensitive people, such as those with asthma or heart conditions, may experience mild respiratory symptoms like coughing or wheezing. Consider reducing strenuous outdoor activities. <br><br>
        Potential Health Impacts: <br>Mild irritation to the respiratory system is possible for sensitive individuals. People with asthma may need to use their inhalers more frequently""","rgba(244, 238, 83, 0.935)"
    elif 101 <= aqi <= 150:
        return """AQI Level: UNHEALTHY FOR SENSITIVE GROUPS<br><br>
        Recommended Measures: <br>Active children and adults, and people with respiratory illness should limit prolonged or heavy exertion outdoors. Consider reducing outdoor activities for everyone. <br><br>
        Potential Health Impacts: <br>Respiratory problems like coughing, wheezing, shortness of breath, and chest tightness are more likely for these groups. People with heart disease may experience angina (chest pain).""","orange"
    elif 151 <= aqi <= 200:
        return """AQI Level: UNHEALTHY<br><br>
        Recommended Measures: <br>Everyone may begin to experience health effects like coughing, wheezing, shortness of breath, chest tightness, and eye irritation. Consider reducing outdoor activities significantly, and people with respiratory or heart disease should restrict strenuous activities.<br><br>
        Potential Health Impacts: <br>The broader population is at risk of experiencing health issues. People with heart disease are particularly vulnerable to angina and other complications.""","red"
    elif 201 <= aqi <= 300:
        return """AQI Level: VERY UNHEALTHY<br><br>
        Health Measures: <br>Health warnings of serious effects are in place. Reduce outdoor activities for everyone. People with respiratory or heart disease should remain indoors and avoid strenuous activity.<br><br>
        Potential Health Impacts: <br>Significant health problems can occur, even in healthy individuals. This includes aggravated asthma, respiratory infections, and heart problems.""","purple"
    else:
        return """AQI Level: HAZAROUS<br><br>
        Recommended Measures: <br>Health alert: everyone may experience more serious health effects. Avoid all outdoor activities.<br><br>
        Potential Health Impacts: <br>This is a severe air quality situation. Everyone is at risk of experiencing respiratory problems, heart attacks, strokes, and even death.""","maroon"
def  convert(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return int(celsius), int(fahrenheit)
@app.route('/get_health_measures', methods=['POST','GET'])
def get_health():
    try:
        if request.method != 'POST':
            return "city not found"
        location = request.form['input_data'].lower()
        url=f"https://api.waqi.info/feed/{location}/?token=3012c977e38a2ef918a762e7654243f2e9b5b7d8"
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        api ="ac82f0ffe2fdf08d7e186def0dd5eb24"

        city = location.title()
        url_temp= f"{base_url}appid={api}&q={location}"
        response = requests.get(url_temp).json()

        
        temp_kelvin = response[ 'main'][ 'temp']
        c,f= convert(temp_kelvin)
        humidity = response['main']['humidity']
        description = response['weather'][0]['description'].title()
        rain = response['rain']['1h'] if 'rain' in response else 0
        wind_speed = response['wind']['speed']
        visibility=response['visibility']

        a=requests.get(url)
        d=a.json()
        aqi=int(str(d['data']['aqi']))
        r,col= get_health_measures(aqi)
        return render_template('weather.html.j2',r=r,col=col,aqi=aqi,c=c,f=f,humidity=humidity,description=description,precipitation=rain,wind_speed=wind_speed,location=city,visibility=visibility)
    except Exception:
        return "city not found"
if __name__ == "__main__":
    app.run(debug=True)



if __name__=='__main__':
    app.run()
