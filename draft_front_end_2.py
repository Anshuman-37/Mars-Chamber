from st_on_hover_tabs import on_hover_tabs
import streamlit as st
import Data_Loader as dl

## Sending the path to the data preprocessing 
path = '/Users/anshuman/Desktop/Personal_Projects /Mars_Chamber/Fake_data.xlsx'; 
## Obtaining the 
dates_array = dl.data_preprocessing(path);

st.set_page_config(layout="wide")

st.markdown("<h1 style='text-align: center;'>Mars Chamber Controll</h1>", unsafe_allow_html=True)
# st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Temperature', 'Pressure', 'Humidity','Uv Light'], 
                         iconName=['T', 'P', 'H','Uv'], default_choice=0)

if tabs =='Temperature':
    st.subheader('Temperature')
    temperature = st.slider('Select the appropriate temperature value (°C): ',-100,100);
    temperature_str = f""" 
    <style>
    p.a {{ 
        font: bold {20}px Courier; 
        }}
    </style>
    <p class="a"> Temperature Sensor Value : {temperature}</p>
    """
    st.markdown(temperature_str, unsafe_allow_html=True);
    for i in dates_array:
        date = i.return_date() ; print(date);
        time,temp = i.return_plot_data_temperature();
        # data = {'time' : time, 'temp':temp}
        data = {'temp':temp}
        st.write(date); st.line_chart(data); 

elif tabs == 'Pressure':
    st.subheader('Pressure')
    pressure = st.slider('Select the appropriate pressure value (mbar) : ',0,1000);
    pressure_str = f""" 
    <style>
    p.a {{ 
        font: bold {20}px Courier; 
        }}
    </style> 
    <p class="a"> Pressure Sensor Value : {pressure}</p>
    """
    st.markdown(pressure_str, unsafe_allow_html=True);
    for i in dates_array:
        date = i.return_date() ; print(date);
        time,pressure = i.return_plot_data_pressure();
        # data = {'time' : time, 'pressure':pressure}
        data=  {'pressure':pressure}
        st.write(date); st.line_chart(data); 

elif tabs == 'Humidity':
    st.subheader('Humidity')
    humidity = st.slider('Select the appropriate humidity (%): ',0,100);
    humidity_str = f"""
    <style>
    p.a {{ 
        font: bold {20}px Courier;
        }}
    </style>
    <p class="a"> Humidity Sensor Value : {humidity}</p>
    """
    st.markdown(humidity_str, unsafe_allow_html=True); #st.write("Humidity Sensors :", humidity)
    for i in dates_array:
        date = i.return_date() ; print(date);
        time,humidity = i.return_plot_data_humidity();
        # data = {'time' : time, 'humidity':humidity}
        data = {'humidity':humidity}
        st.write(date); st.line_chart(data);
   
elif tabs == 'Uv Light':
    #Uv Light
    st.subheader('UV light')
    uv_light= st.slider("Toggle the light 0 for OFF and 1 for ON :", 0, 1, 1)
    uv_light_str = f""" 
    <style>
    p.a {{ 
        font: bold {20}px Courier; 
        }}
    </style>
    <p class="a"> UV Light Sensor Status : {uv_light}</p>
    """
    st.markdown(uv_light_str, unsafe_allow_html=True); #st.write("UV Light :", uv_light)
    for i in dates_array:
        date = i.return_date() ; print(date);
        time,uv_light = i.return_plot_data_uv_light();
        # data = {'time' : time, 'uv_light':uv_light}
        data = {'uv_light':uv_light}
        st.write(date); st.line_chart(data);

