import streamlit as st
import requests
import json
from PIL import Image
import streamlit.components.v1 as components

import base64
import imghdr
import streamlit as st

def add_bg_from_local(image_file):
    # Determine the MIME type of the image file
    image_type = imghdr.what(image_file)
    if not image_type:
        raise ValueError("Invalid image file")

    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    # Set the background image using inline CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('data:image/{image_type};base64,{encoded_string}');
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
st.set_page_config(page_title="AAKASHवाणी", page_icon=":partly_sunny:", layout="wide")

image = Image.open('logo.png')
st.image(image,width=300)
st.title("AAKASHवाणी")
st.subheader("Where weather meets technology!")

url = "https://weatherapi-com.p.rapidapi.com/current.json"

headers = {
    'X-RapidAPI-Key': '9313132d8bmsh3b12348597c1003p19f0dcjsn74c0ee15b248',
    'X-RapidAPI-Host': 'weatherapi-com.p.rapidapi.com'
}

location = st.text_input("Enter the location", "Patiala")
querystring = {"q":{location}}

response = requests.request("GET", url, headers=headers, params=querystring)
result = response.text

data = json.loads(result)

st.json(data)

col1, col2 = st.columns(2)

with col1:
    st.write(f'Name: {data["location"]["name"]}')
    st.write(f'Region: {data["location"]["region"]}')
    st.write(f'Country: {data["location"]["country"]}')
    st.write(f'Local Time: {data["location"]["localtime"]}')
    st.metric(label="wind_kph", value= f'{data["current"]["wind_kph"]}')
    st.write(f'Feels like: {data["current"]["feelslike_c"]} ℃')

with col2: 
    st.write(f'Temp in Celsius: {data["current"]["temp_c"]}')
    st.write(f'Temp in Farenheit: {data["current"]["temp_f"]}')
    st.write(f'Condition: {data["current"]["condition"]["text"]}')
    st.image(f'http:{data["current"]["condition"]["icon"]}')
    st.metric(label = "Humidity", value = f'{data["current"]["humidity"]}')
    
st.info('AAKASHवाणी ☀️  is our Computer Graphics Project. It is aimed at providing visualizations of the real-time weather conditions using opengl concepts taught to us in this subject.')

import datetime

# Convert the localtime string to a datetime object
localtime = datetime.datetime.strptime(data["location"]["localtime"], "%Y-%m-%d %H:%M")

# Set the start and end times of the desired interval
start_time = datetime.time(5, 30)
end_time = datetime.time(19, 30)

# Check if the localtime falls within the interval
if start_time <= localtime.time() <= end_time:
    if data["current"]["precip_mm"]<=0.1:
        video_file = open('./animations/sun_no_rain.mp4', 'rb')
    else:
        video_file = open('./animations/sun_rain.mp4', 'rb')

else:
    if data["current"]["precip_mm"]<=0.1:
        video_file = open('./animations/no_sun_no_rain.mp4', 'rb')

    else:
        video_file = open('./animations/no_sun_rain.mp4', 'rb')


video_bytes = video_file.read()
st.video(video_bytes)

add_bg_from_local("wallpaper.png")

