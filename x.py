import streamlit as st
import Data_Loader as dl

## Sending the path to the data preprocessing 
path = '/Users/anshuman/Desktop/Personal_Projects /Mars_Chamber/Fake_data.xlsx'; 
## Obtaining the 
dates_array = dl.data_preprocessing(path);
st.set_page_config(layout="wide")
st.cache()

## Sensors Controll
## The Header for the application
st.markdown("<h1 style='text-align: center;'>Mars Chamber Controll</h1>", unsafe_allow_html=True)
# st.text("");st.text("");
col1,col2,col3 = st.columns([2,2,3],gap="large")

with col1:
    ## Temperature
    # st.subheader('Temperature(°C)')
    temperature = st.slider('Temperature (°C)',-100,100);
    temp_manual = st.text_input('Temperature manuall (Type 0 to use slider value):',value = 0);
    print(type(temperature),temperature,type(temp_manual))
    if int(temp_manual)!=0: temperature = temp_manual; 
    temperature_str = f""" 
    <style>
    p.a {{ 
        font: bold {14}px Courier; 
        }}
    </style>
    <p class="a"> Temperature Sensor Value : {temperature}</p>
    """
    st.markdown(temperature_str, unsafe_allow_html=True); # st.write(Temperature Sensor Value : ",temperature) 

    ## Pressure
    # st.subheader('Pressure')
    st.text("");st.text("");
    pressure = st.slider('Pressure (mbar) : ',0,1000);
    prep_manual = st.text_input('Pressure manuall (Type - 1 to use slider value) :',value = -1);
    print(type(pressure),pressure,type(prep_manual))
    if int(prep_manual)!=-1: pressure = prep_manual; 
    pressure_str = f""" 
    <style>
    p.a {{ 
        font: bold {14}px Courier; 
        }}
    </style> 
    <p class="a"> Pressure Sensor Value : {pressure}</p>
    """
    st.markdown(pressure_str, unsafe_allow_html=True); #st.write("Pressure Sensors :", pressure)

    # Humidity
    # st.subheader('Humidity')
    st.text("");st.text("");
    humidity = st.slider('Humidity (%): ',0,100);
    humi_manual = st.text_input('Humidity (Type - 1 to use slider value) :',value = -1);
    print(type(pressure),pressure,type(prep_manual))
    if int(humi_manual)!=-1: humidity = humi_manual;
    humidity_str = f"""
    <style>
    p.a {{ 
        font: bold {14}px Courier;
        }}
    </style>
    <p class="a"> Humidity Sensor Value : {humidity}</p>
    """
    st.markdown(humidity_str, unsafe_allow_html=True); #st.write("Humidity Sensors :", humidity)
    
    
    #Uv Light
    # st.subheader('UV light')
    st.text("");st.text("");
    uv_light = st.slider("UV light 0 for OFF and 1 for ON :", 0, 1, 1)
    uv_light_str = f""" 
    <style>
    p.a {{ 
        font: bold {14}px Courier; 
        }}
    </style>
    <p class="a"> UV Light Sensor Status : {uv_light}</p>
    """
    st.markdown(uv_light_str, unsafe_allow_html=True); #st.write("UV Light :", uv_light)


### Sensors data
with col2:
    st.subheader('Temperature');

### Plots
with col3:

    for i in dates_array:
        date = i.return_date(); print(date);
        time,temp = i.return_plot_data_temperature();
        data = {'time' : time, 'temp':temp}
        st.write(date); st.line_chart(data); 
    
    for i in dates_array:
        date = i.return_date() ; print(date);
        time,pressure = i.return_plot_data_pressure();
        data = {'time' : time, 'pressure':pressure}
        st.write(date); st.line_chart(data); 
    
    for i in dates_array:
        date = i.return_date() ; print(date);
        time,humidity = i.return_plot_data_humidity();
        data = {'time' : time, 'humidity':humidity}
        st.write(date); st.line_chart(data);
    
    for i in dates_array:
        date = i.return_date() ; print(date);
        time,uv_light = i.return_plot_data_uv_light();
        data = {'time' : time, 'uv_light':uv_light}
        st.write(date); st.line_chart(data); 

