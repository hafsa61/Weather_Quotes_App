import requests
import streamlit as st
import pandas as pd
from datetime import datetime
from config import API_KEY

st.set_page_config(page_title="Weather & Quotes App", page_icon="🌦️", layout="centered")

def local_css(file_name):
    with open(file_name, encoding="utf-8") as f:  
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")


st.markdown("<h1>🌦️ Weather & Quotes App 💬</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    city = st.text_input("", placeholder="Enter a city name...")
with col2:
    get_data = st.button("Get Weather & Quote")

if get_data:
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    wres = requests.get(weather_url)
    wdata = wres.json()

    if wres.status_code == 200:
        temp = wdata['main']['temp']
        condition = wdata['weather'][0]['description']

        qres = requests.get("https://zenquotes.io/api/random")
        qdata = qres.json()
        quote = qdata[0]['q']
        author = qdata[0]['a']

        st.markdown(f"""
        <div class='card'>
            <h3>🌤️ Weather in {city.capitalize()}</h3>
            <p><b>Temperature :</b> {temp} °C</p>
            <p><b>Condition :</b> {condition.capitalize()}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='card'>
            <h3>💬 Quote of the Moment</h3>
            <p class='quote'>"{quote}"</p>
            <p class='author'>— {author}</p>
        </div>
        """, unsafe_allow_html=True)

        history = {
            "DateTime": [datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            "City": [city],
            "Temperature": [temp],
            "Condition": [condition],
            "Quote": [quote],
            "Author": [author]
        }
        df = pd.DataFrame(history)
        with open("history.csv", "a", encoding="utf-8", newline="") as f:
            df.to_csv(f, header=f.tell() == 0, index=False)

        st.markdown("<p class='save-badge'> Saved to history!</p>", unsafe_allow_html=True)
    else:
        st.error("❌ Could not fetch weather data. Check city name.")

