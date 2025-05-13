import pandas as pd
import streamlit as st
import requests
from datetime import datetime
#from dotenv import load_dotenv

#load_dotenv()
#API_key = os.getenv('api_key')

API_key = st.secrets['api_key']

def tempo_citta(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_key}'
    result = requests.get(url)
    json = result.json()
    return json


def clima(citta):
    json = tempo_citta(citta)
    clima_ = json['weather'][0]['description']
    temperatura = round(json['main']['temp'] - 273.15,2)
    temp_percepita = round(json['main']['feels_like'] - 273.15, 2)   
    temp_max = round(json['main']['temp_max'] - 273.15, 2)
    temp_min = round(json['main']['temp_min'] - 273.15, 2)
    vento = json['wind']['speed']
    alba = datetime.fromtimestamp(json['sys']['sunrise'])
    alba = pd.Timestamp(alba).time()
    tramonto = datetime.fromtimestamp(json['sys']['sunset'])
    tramonto = pd.Timestamp(tramonto).time()
    result = [clima_,temperatura,temp_percepita,temp_max,temp_min,vento,alba,tramonto]
    return result

def mappa(citta):
    json = tempo_citta(citta)
    latitudine = json['coord']['lat']
    longitudine = json['coord']['lon']
    df = pd.DataFrame({'lat' : [latitudine] , 'lon' : [longitudine]}, columns=['lat', 'lon'])
    return df

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://cdn.pixabay.com/photo/2020/07/19/14/15/sky-5420151_1280.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )


def main():
    st.set_page_config(page_title='Previsioni', layout='wide')
    st.title("PREVISIONE METEO")
    st.divider()
    
    add_bg_from_url()

    city_name = st.text_input("Seleziona la città", "Bologna")
    st.divider()
   
    col1,col2 = st.columns(2)
    with col1:

        result = clima(city_name)
        clima_ = result[0]
        temperatura = result[1]
        temp_percepita = result[2]
        temp_max = result[3]
        temp_min = result[4]
        vento = result[5]
        alba = result[6]
        tramonto = result[7]

        st.text(f'Clima: {clima_}')
        st.text(f'Temperatura: {temperatura}°')
        st.text(f'Temperatura Percepita: {temp_percepita}°')
        st.text(f'Temperatura Massima: {temp_max}°')
        st.text(f'Temperatura Minimo: {temp_min}°')
        st.text(f'Velocità Vento: {vento} m/s')
        st.text(f'Ora Alba: {alba}')
        st.text(f'Ora Tramonto: {tramonto}')
    
    with col2:
        df = mappa(city_name)
        st.map(data=df, size=500)

if __name__ == "__main__":
    main()
