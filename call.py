#%%
## This will call the functions in the test.py file
import test as Sensors
from datetime import datetime 
import matplotlib.pyplot as plt
from serial.tools import list_ports
import time
import csv
import pandas as pd 
from time import mktime


## Hashmap to store the data for the values
data = {'time':[],'air_humi':[],'air_temp':[],'table_temp':[],'pressure':[]}; 

## Obtaining all the ports 
port = list(list_ports.comports())
## Creating a sensors object
s = Sensors.sensors();
i = 0;
df = pd.DataFrame(columns=data.keys())
lst  = []
## When envoked for the first time to measure time difference
start_time = time.localtime(); 
while(True):
    ## Getting the current time for the plot on the graph
    ## Gettin the time for excel
    t = time.localtime(); excel_time = time.strftime('%Y/%m/%d %H:%M:%S');
    
    start = datetime.fromtimestamp(mktime(start_time)); now = datetime.fromtimestamp(mktime(t));
    # duration = datetime.combine(date.min, t) - datetime.combine(date.min, starting_time)
    x = int(time.strftime('%H%M%S',t)); 
    print('time_elapsed ',now-start);
    time.sleep(.01)
    sensor_res = []
    ## Setting the sensors port 
    s.set_sensors_port(port);
    ## Setting the sensor values
    s.set_sensor_data();
    ## Printing the data for the sensors 
    humi,temp = s.return_sensor_data();

    try:
        ## Get the values of the sensors
        air_humi,air_temp = humi.return_sensors_values();
        # Check whether there is a string or not
        try : 
            air_humi = float(air_humi); air_temp = float(air_temp);
        except:
            air_humi = float("nan") ; air_temp = float("nan");  
        ## printing the result
        print('Sensor values for Vaisala Humidity - > ', air_humi,' Temperature - > ',air_temp);
        ## Append the data to the dictionary 
        data['air_humi'].append(air_humi); data['air_temp'].append(air_temp);

    except:
        ## Assigne the values to the sensors
        air_humi = float("nan") ; air_temp = float("nan");
        ## The sensor is not present
        print('Humidity Sensor Not Present');
        ## Append the data to the dictionary 
        data['air_humi'].append(air_humi); data['air_temp'].append(air_temp);

    try: 
        ## Obtain the sensors value
        table_temp = temp.return_sensors_values();
        ## Check whether the values obtained are correct or not
        print
        try : 
            table_temp = float(table_temp);
        except:
            table_temp = float("nan"); 
        ## Printing the result on the console 
        print('Sensor Value for Simex Temp Table Temp - >',table_temp);
        ## Append the data to the dictionary
        data['table_temp'].append(table_temp);

    except:
        ## Assign the value to the sensors
        table_temp = float("nan"); 
        ## The sensor is not present
        print('Temperature Sensor Not present');
        ## Append to the dictionary
        data['table_temp'].append(table_temp);
    
    ## Assigning nan to the pressure 
    pressure = float("nan");
    ## Appending the pressure sensor to the data 
    data['pressure'].append(pressure);
    ## Appending time to the data
    alpha = str(now - start);# aplha =str(alpha)
    data['time'].append(alpha);
    
    ## Plot for Pressure
    plt.subplot(1,2,1)
    plt.title('Humidity VS Time Elapsed')
    plt.plot(data['time'][:],data['air_humi'][:],color = 'red');
    plt.ylabel('Humidity in Percentage')
    plt.xlabel('Time Elapsed (Hours:Minutes:Seconds)')
    plt.xticks(rotation=40, ha='right')
    # plt.locator_params(axis='x', nbins=10*((i/10) + 1))
    ticks_only = [data['time'][x] for x in range(1,len(data['time']),int(len(data['time'])/8)+1)] 
    # ticks_only.append(data['time'][-1])
    plt.xticks(ticks_only)
    plt.pause(0.05)
    
    ## Plot for Temperature
    plt.subplot(1,2,2)
    plt.title('Temperature VS Time Elapsed')
    plt.plot(data['time'][:],data['air_temp'][:],color = 'black');
    plt.xticks(rotation=40, ha='right')
    plt.xlabel('Time Elapsed (Hours:Minutes:Seconds)')
    plt.ylabel('Temperature in Celcius')
    # plt.locator_params(axis='x', nbins=10*((i/10) + 1))
    ticks_only = [data['time'][x] for x in range(1,len(data['time']),int(len(data['time'])/8)+1)]
    # ticks_only.append(data['time'][-1])
    plt.xticks(ticks_only)
    plt.pause(0.05)
    ## Appending the data to the list
    sensor_res.append(excel_time); sensor_res.append(air_humi); sensor_res.append(air_temp); sensor_res.append(table_temp); sensor_res.append(pressure); 
    # print(i)
    ## Creating the list for the sensor 
    lst.append(sensor_res);

# print(lst)
df = pd.DataFrame(lst, columns = data.keys())
print(df)
df.to_csv('IDK.csv', index=False)
plt.show();
# %%



### 
'''
Things planned for today
1. Getting the date and time in the excel file
2. Getting the hours,minutes and seconds in the dictionary 
3. How long to read the sensor's data Can't keep the code running forever
'''
###