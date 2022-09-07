## This will call the functions in the test.py file
import test as Sensors
import datetime as dt
import matplotlib.pyplot as plt
from serial.tools import list_ports
import time
import csv
import pandas as pd 

## Hashmap to store the data for the values
data = {'air_humi':[],'air_temp':[],'table_temp':[],'pressure':[],'time':[]}; 

## Obtaining all the ports 
port = list(list_ports.comports())
## Creating a sensors object
s = Sensors.sensors();
i = 10;
df = pd.DataFrame(columns=data.keys())
lst  = []
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1);
xs = []; ys = [];

while(i<1000):
    ## Getting data 
    hour,mins,sec = map(str, time.strftime("%H %M %S").split())
    t = hour+mins+sec
    print(hour,mins,sec)
    # time.sleep(60)
    sensor_res = []
    ## Setting the sensors port 
    s.set_sensors_port(port);
    ## Setting the sensor values
    s.set_sensor_data();
    ## Printing the data for the sensors 
    humi,temp = s.return_sensor_data();

    try:
        air_humi,air_temp = humi.return_sensors_values();
        
        try : 
            air_humi = float(air_humi); air_temp = float(air_temp);
        except:
            air_humi = float("nan") ; air_temp = float("nan");  
        
        print('Sensor values for Vaisala Humidity - > ', air_humi,' Temperature - > ',air_temp);
        data['air_humi'].append(air_humi); data['air_temp'].append(air_temp);

    except:
        print('Humidity Sensor Not Present');
        data['air_humi'].append(air_humi); data['air_temp'].append(air_temp);

    try: 
        table_temp = temp.return_sensors_values();
        
        try : 
            table_temp = float(table_temp);
        except:
            table_temp = float("nan"); 
        
        print('Sensor Value for Simex Temp Table Temp - >',table_temp);
        data['table_temp'].append(table_temp);

    except:
        table_temp = float("nan"); 
        print('Temperature Sensor Not present');
        data['table_temp'].append(table_temp);

    pressure = float("nan");
    data['pressure'].append(pressure);
    data['time'].append(time.strftime("%H:%M:%S"));
    if( i % 100 == 0):
        ## Plotting the graphs/storing the concurrent result
        plt.plot(data['time'][-20:],data['air_humi'][-20:]); 
        plt.pause(0.05)

    plt.show()
    ## Appending the data to the list
    sensor_res.append(air_humi); sensor_res.append(air_temp); sensor_res.append(table_temp); sensor_res.append(pressure); sensor_res.append(t);
    
    ## Creating the  
    lst.append(sensor_res);
    i = i+10;

# print(lst)
df = pd.DataFrame(lst, columns = data.keys())
print(df)
df.to_csv('IDK.csv', index=False)
