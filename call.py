
## This will call the functions in the test.py file
import test as Sensors
from datetime import datetime 
import matplotlib.pyplot as plt
from serial.tools import list_ports
import time
import csv
import pandas as pd 
from time import mktime
from threading import Thread
import concurrent.futures

def data_plot(x,y,x_label,y_label,type):
    ''' Function to make plot for the data for multiple threads '''
    if type == 0: plt.title('Humidity VS Time Elapsed');
    if type == 1: plt.title('Temperature VS Time Elapsed');
    if type == 2: plt.title('Table Temperature VS Time Elapsed');
    if type == 3: plt.title('Pressure VS Time Elapsed');

    plt.plot(x,y,color = 'red');
    plt.ylabel(y_label);    plt.xlabel(x_label);
    plt.xticks(rotation=40, ha='right')
    ticks_only = [x for i in range(1,len(x),int(len(x)/8)+1)] 
    # ticks_only.append(data['time'][-1])
    plt.xticks(ticks_only)
    plt.pause(0.05)

def humi_data_cleaning(humi_sensor):
    ''' 
    Params - Humidity Sensor
    Result - Will return the cleaned data from the humi_sensor object back to the code 
    '''
    try:
        ## Get the values of the sensors
        air_humi,air_temp = humi_sensor.return_sensors_values();
        # Check whether there is a string or not
        try : 
            air_humi = float(air_humi); air_temp = float(air_temp);
        except:
            air_humi = float("nan") ; air_temp = float("nan");  
        ## printing the result
        print('Sensor values for Vaisala Humidity - > ', air_humi,' Temperature - > ',air_temp);
    except:
        ## Assigne the values to the sensors
        air_humi = float("nan") ; air_temp = float("nan");
        ## The sensor is not present
        print('Humidity Sensor Not Present');
    return air_humi,air_temp; 

def table_temp_data_cleaning(temp_sensor):
    '''
    Params - Temperature Sensor
    Result - Will return the cleaned data from the table temperature senors object back to the code
    '''
    try: 
        ## Obtain the sensors value
        table_temp = temp_sensor.return_sensors_values();
        ## Check whether the values obtained are correct or not
        try : 
            table_temp = float(table_temp);
        except:
            table_temp = float("nan"); 
        ## Printing the result on the console 
        print('Sensor Value for Simex Temp Table Temp - >',table_temp);

    except:
        ## Assign the value to the sensors
        table_temp = float("nan"); 
        ## The sensor is not present
        print('Temperature Sensor Not present');
    
    return table_temp;


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
    # time.sleep(0.5)
    t = time.localtime(); excel_time = time.strftime('%Y/%m/%d %H:%M:%S');
    
    start = datetime.fromtimestamp(mktime(start_time)); now = datetime.fromtimestamp(mktime(t));

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
    
    ## Executing the threads
    with concurrent.futures.ThreadPoolExecutor() as exe:
        humi_sensor = exe.submit(humi_data_cleaning, humi)
        air_humi,air_temp= humi_sensor.result();
        temp_sensor = exe.submit(table_temp_data_cleaning, temp)
        table_temp = temp_sensor.result();

    # appending the data
    data['air_humi'].append(air_humi); data['air_temp'].append(air_temp); data['table_temp'].append(table_temp);

    
    ## Assigning nan to the pressure 
    pressure = float("nan");
    ## Appending the pressure sensor to the data 
    data['pressure'].append(pressure);
    ## Appending time to the data
    alpha = str(now - start);# aplha =str(alpha)
    data['time'].append(alpha);
    
    # ## Plot for Humidity from Vaisala 
    # plt.subplot(1,3,1)
    # plt.title('Humidity VS Time Elapsed')
    # plt.plot(data['time'][:],data['air_humi'][:],color = 'red');
    # plt.ylabel('Humidity in Percentage')
    # plt.xlabel('Time Elapsed (Hours:Minutes:Seconds)')
    # plt.xticks(rotation=40, ha='right')
    # # plt.locator_params(axis='x', nbins=10*((i/10) + 1))
    # ticks_only = [data['time'][x] for x in range(1,len(data['time']),int(len(data['time'])/8)+1)] 
    # # ticks_only.append(data['time'][-1])
    # plt.xticks(ticks_only)
    # plt.pause(0.05)


    # ## Plot for Temperature from Viasala 
    # plt.subplot(1,3,2)
    # plt.title('Temperature VS Time Elapsed')
    # plt.plot(data['time'][:],data['air_temp'][:],color = 'black');
    # plt.xticks(rotation=40, ha='right')
    # plt.xlabel('Time Elapsed (Hours:Minutes:Seconds)')
    # plt.ylabel('Temperature in Celcius')
    # # plt.locator_params(axis='x', nbins=10*((i/10) + 1))
    # ticks_only = [data['time'][x] for x in range(1,len(data['time']),int(len(data['time'])/8)+1)]
    # # ticks_only.append(data['time'][-1])
    # plt.xticks(ticks_only)
    # plt.pause(0.05)

    # ## Plot for Table Temperature from Simex
    # plt.subplot(1,3,3)
    # plt.title('Table Temperature VS Time Elapsed')
    # plt.plot(data['time'][:],data['table_temp'][:],color = 'blue');
    # plt.xticks(rotation=40, ha='right')
    # plt.xlabel('Time Elapsed (Hours:Minutes:Seconds)')
    # plt.ylabel('Temperature in Celcius')
    # # plt.locator_params(axis='x', nbins=10*((i/10) + 1))
    # ticks_only = [data['time'][x] for x in range(1,len(data['time']),int(len(data['time'])/8)+1)]
    # # ticks_only.append(data['time'][-1])
    # plt.xticks(ticks_only)
    # plt.pause(0.05)
    
    # with concurrent.futures.ThreadPoolExecutor() as exe:
    #     humi_plot = exe.submit(data_plot,data['time'][:],data['air_humi'][:],'Time Elapsed (Hours:Minutes:Seconds)','Humidity in Percentage',0)
    #     humi_plot.result() 
    ## code to support multithreading 
    
    ## Create a thread
    # plot_1 = Thread(target = data_plot, \
    #     args = (data['time'][:],data['air_humi'][:],'Time Elapsed (Hours:Minutes:Seconds)','Humidity in Percentage',0));
    
    ## Create a thread
    # plot_2 = Thread(target = data_plot, \
    #     args = (data['time'][:],data['air_temp'][:],'Time Elapsed (Hours:Minutes:Seconds)','Temperature in Celcius',1));
    ## Start the threads
    # plot_1.start(); plot_2.start();
    ## Join the threads 
    # plot_1.join(); plot_2.join();

    # Appending the data to the list
    sensor_res.append(excel_time); sensor_res.append(air_humi); sensor_res.append(air_temp); sensor_res.append(table_temp); sensor_res.append(pressure); 
    # print(i)
    ## Creating the list for the sensor 
    lst.append(sensor_res);

print(lst)
df = pd.DataFrame(lst, columns = data.keys())
print(df)
df.to_csv('IDK.csv', index=False)
plt.show();


