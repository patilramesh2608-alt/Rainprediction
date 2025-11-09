import streamlit as st
import requests
import pickle
import plotly.express as px
import pandas as pd


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

data = pd.read_csv("./data.csv")


def get_weather():
    api_url = 'https://api.open-meteo.com/v1/forecast?latitude=19.0728&longitude=72.8826&hourly=temperature_2m,relative_humidity_2m,precipitation,weather_code,temperature_80m&daily=sunrise,sunset'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['hourly']['temperature_80m'][0]
        return temperature
    else:
        return None

st.title("Mumbai Weather Insights")

nav = st.sidebar.radio("Navigation", ["Home","Prediction", "Past Data"])

if nav == "Home":
    st.write("Welcome to Mumbai Weather Insights – your comprehensive weather companion for the vibrant city of Mumbai! Peer into the future with our advanced rainfall prediction model and gain a deeper understanding of Mumbai's climate over time and explore how it has evolved.")
    
    
    temperature = get_weather()
    if temperature is not None:
       st.markdown(f"<p style='font-size:24px; font-weight:bold;'>Currently {temperature}°C</p>", unsafe_allow_html=True)

    else:
        st.error("Failed to fetch weather data. Please try again later.")
    
    
    st.image("mum2.jpeg", width=700)

        
if nav== "Prediction":
    st.write("Enter environmental parameters for personalized rainfall predictions.")
    def classify(num):
        if num[0]==0:
            return "No rain expected."
        elif num[0]<5:
            return f"Light rain expected with precipitation of {num[0]}mm"
        elif num[0]<15:
            return f"Moderate rain expected with precipitation of {num[0]}mm"
        else:
            return f"Heavy rain expected with precipitation of {num[0]}mm"
            
    dew = st.text_input("Dew")   
    temp= st.text_input("Temperature (°C)")  
    hum= st.text_input("Humidity (%)")  
    pre= st.text_input("Surface Pressure (Pa)")  
    ws= st.text_input("Wind speed (km/h)")  
    inputs=[[dew,temp,hum,pre,ws]]
    if st.button('Predict'):
        st.success(classify(model.predict(inputs)))
    
if nav == "Past Data":
    st.write("Mumbai Rainfall Analysis for past 10 years")
   
    year = st.sidebar.number_input("Select Year (2013 to 2022)", min_value=2013, max_value=2022)
    filtered_data = data[data['time'].str.startswith(str(year))]


    monthly_rainfall = filtered_data.groupby(filtered_data['time'].str[5:7])['precipitation (mm)'].sum().reset_index()
    monthly_rainfall.columns = ['Month', 'Total Rainfall (mm)']

    
    fig = px.bar(monthly_rainfall, x='Month', y='Total Rainfall (mm)', labels={'Month': 'Month', 'Total Rainfall (mm)': 'Total Rainfall (mm)'}, title=f"Mumbai Rainfall Analysis for the Year {year}")
    st.plotly_chart(fig)