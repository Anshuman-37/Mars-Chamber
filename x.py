import streamlit as st
import Data_Loader as dl

## Sending the path to the data preprocessing 
path = '/content/Fake_data.xlsx'; 
## Obtaining the 
dates_array = dl.data_preprocessing(path);

st.cache()


## The Header for the application
st.markdown("<h1 style='text-align: center;'>Mars Chamber Controll</h1>", unsafe_allow_html=True)
st.text("");st.text("")
col1, col2, col3, col4 = st.columns(4)

with col1:
    ## Temperature
    st.subheader('Temperature')
    temperature = st.slider('Select the appropriate temperature value (°C): ',-100,100);
    temperature_str = f""" 
    <style>
    p.a {{ 
        font: bold {14}px Courier; 
        }}
    </style>
    <p class="a"> Temperature Sensor Value : {temperature}</p>
    """
    st.markdown(temperature_str, unsafe_allow_html=True); # st.write(Temperature Sensor Value : ",temperature)
    for i in dates_array:
        date = i.return_date() ; print(date);
        st.write(date);

with col2:
    ## Pressure
    st.subheader('Pressure')
    pressure = st.slider('Select the appropriate pressure value (mbar) : ',0,1000);
    pressure_str = f""" 
    <style>
    p.a {{ 
        font: bold {14}px Courier; 
        }}
    </style> 
    <p class="a"> Pressure Sensor Value : {pressure}</p>
    """
    st.markdown(pressure_str, unsafe_allow_html=True); #st.write("Pressure Sensors :", pressure)

with col3:
    ## Humidity
    st.subheader('Humidity')
    humidity = st.slider('Select the appropriate humidity (%): ',0,100);
    humidity_str = f"""
    <style>
    p.a {{ 
        font: bold {14}px Courier;
        }}
    </style>
    <p class="a"> Humidity Sensor Value : {humidity}</p>
    """
    st.markdown(humidity_str, unsafe_allow_html=True); #st.write("Humidity Sensors :", humidity)
with col4:
    ## Uv Light
    st.subheader('UV light')
    uv_light= st.slider("Toggle the light 0 for OFF and 1 for ON :", 0, 1, 1)
    uv_light_str = f""" 
    <style>
    p.a {{ 
        font: bold {14}px Courier; 
        }}
    </style>
    <p class="a"> UV Light Sensor Status : {uv_light}</p>
    """
    st.markdown(uv_light_str, unsafe_allow_html=True); #st.write("UV Light :", uv_light)
