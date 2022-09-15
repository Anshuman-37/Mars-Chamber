## This will call the functions in the test.py file

## Import libraries and all the other useless step
import test as Sensors
from datetime import datetime 
# import matplotlib.pyplot as plt
from serial.tools import list_ports
import time
# import csv
# import pandas as pd 
from time import mktime
# from threading import Thread
import concurrent.futures
import RPi.GPIO as GPIO



# ## Function to plot the graph over the server side
# def data_plot(x,y,x_label,y_label,type):
#         '''
#         Params - x , y, label of x , label of y, which graph to show 
#         Result - Function to make plot for the data for multiple threads 
#         '''

#         ## If statements according to the graphs
#         if type == 0: plt.title('Humidity VS Time Elapsed');
#         if type == 1: plt.title('Temperature VS Time Elapsed');
#         if type == 2: plt.title('Table Temperature VS Time Elapsed');
#         if type == 3: plt.title('Pressure VS Time Elapsed');
        
#         ## Plotting the graphs according the color 
#         plt.plot(x,y,color = 'red');
#         plt.ylabel(y_label);    plt.xlabel(x_label);
#         plt.xticks(rotation=40, ha='right')

#         ## To only keep important labels in the ticks (it only keep 8 values in the graph)
#         ticks_only = [x for i in range(1,len(x),int(len(x)/8)+1)]  # ticks_only.append(data['time'][-1])
#         plt.xticks(ticks_only)
        
#         ## To plot in real time
#         plt.pause(0.05)


## Class to handle all the main functions 
class Main:
    '''This class will take care of all the main function'''
    def __init__(self):
        ''' Intiallize the main variable to store the data in the class '''
        ## Hash map to store all the data in the map
        self.data = {'time':[],'air_humi':[],'air_temp':[],'table_temp':[],'pressure':[]};
        ## To store the data in list format for the csv file
        self.lst = [];
    

    def humi_data_cleaning(self,humi_sensor):
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

    def table_temp_data_cleaning(self,temp_sensor):
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
    
    def read_sensor_values(self,port):
        '''
        Params - Self reference , The list of all the comms connected over the port
        Result - Updates the sensor values, and prints them on the console
        '''
        ## Obtaining all the ports 
        self.ports = port; 
        
        ## Creating an object of the sensors to get the values from the sensor
        self.s = Sensors.sensors();
        
        ## Getting the start time from the local time on the computer
        self.start_time = time.localtime(); 

        while(True):
            
            ## Getting the current time and the time to save the data in the excel
            curr_time = time.localtime(); excel_time = time.strftime('%Y/%m/%d %H:%M:%S');

            ## The start time indicates when the code started now refers to the current. Need this to obtain the elapsed time    
            start = datetime.fromtimestamp(mktime(self.start_time)); now = datetime.fromtimestamp(mktime(curr_time));

            ## Print the elapsed time
            print('Time_elapsed -> ',now-start);

            ## Local variable to store the result of the loop
            sensor_res = []

            ## Setting the sensors port 
            self.s.set_sensors_port(self.ports);
            ## Setting the sensor values (It gets the value of the sensor data internally)
            self.s.set_sensor_data();
            ## Obataining the data for the sensors 
            self.humi,self.temp = self.s.return_sensor_data();

            ## Executing the threads concurrently to obtain the cleaned data
            with concurrent.futures.ThreadPoolExecutor() as exe:
                humi_sensor = exe.submit(self.humi_data_cleaning, self.humi)
                air_humi,air_temp= humi_sensor.result();
                temp_sensor = exe.submit(self.table_temp_data_cleaning, self.temp)
                table_temp = temp_sensor.result();
            
            # appending the data in the hashmap stored
            self.data['air_humi'].append(air_humi); 
            self.data['air_temp'].append(air_temp); 
            self.data['table_temp'].append(table_temp);
        
            ## Assigning nan to the pressure 
            pressure = float("nan");
            ## Appending the pressure sensor to the data 
            self.data['pressure'].append(pressure);
            ## Converting the elapsed time to string and Appending time to the data
            alpha = str(now - start); 
            self.data['time'].append(alpha);

            # Appending the data to the list
            sensor_res.append(excel_time); 
            sensor_res.append(air_humi); 
            sensor_res.append(air_temp); 
            sensor_res.append(table_temp); 
            sensor_res.append(pressure); 
            # print(i)
            ## Creating the list for the sensor 
            self.lst.append(sensor_res);

    def OnOff_relay(self,target_temp):
        '''
        Params - The target temperature and the current temperature of the sensor
        Result - Sets the relay status and the current values regarding it
        '''
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(4, GPIO.OUT) #set Relay 1 output
        GPIO.setup(17, GPIO.OUT) #set Relay 2 output

        #Pi Zero users do not need to configure the pins for Relays 3 & 4, these are unused.
        GPIO.setup(27, GPIO.OUT) #set Relay 3 output
        GPIO.setup(22, GPIO.OUT) #set Relay 4 output

        if (target_temp-1) > self.data['table_temp'][-1]:
            GPIO.output(4, GPIO.HIGH) #turn relay 1 on
            print('Task still in execution')
        else:
            GPIO.output(4, GPIO.LOW) # turn relay 0 off
            print('This is done')
    
    def concurent(self,ports,target_temp):
        '''
        Params - Self Reference, The target tempereature
        Result - Concurrently runs the sensor value and the relays 
        '''
        with concurrent.futures.ThreadPoolExecutor() as exe:
            sensor_values = exe.submit(self.read_sensor_values,ports)
            on_off = exe.submit(self.OnOff_relay,target_temp)
            on_off.result();sensor_values.result();



port = list(list_ports.comports())
x = Main();


    
x.concurent(port,35);
# ## Obtaining all the ports 
# port = list(list_ports.comports())
# ## Creating a sensors object
# s = Sensors.sensors();
# i = 0;
# # df = pd.DataFrame(columns=data.keys())
# lst  = []
# ## When envoked for the first time to measure time difference
# start_time = time.localtime(); 

# while(True):
#     ## Getting the current time for the plot on the graph
#     ## Gettin the time for excel
#     # time.sleep(0.5)
#     t = time.localtime(); excel_time = time.strftime('%Y/%m/%d %H:%M:%S');
    
#     start = datetime.fromtimestamp(mktime(start_time)); now = datetime.fromtimestamp(mktime(t));

#     x = int(time.strftime('%H%M%S',t)); 
#     print('time_elapsed ',now-start);
#     # time.sleep(.01)
#     sensor_res = []
#     ## Setting the sensors port 
#     s.set_sensors_port(port);
#     ## Setting the sensor values
#     s.set_sensor_data();
#     ## Printing the data for the sensors 
#     humi,temp = s.return_sensor_data();
    
#     ## Executing the threads
#     with concurrent.futures.ThreadPoolExecutor() as exe:
#         humi_sensor = exe.submit(humi_data_cleaning, humi)
#         air_humi,air_temp= humi_sensor.result();
#         temp_sensor = exe.submit(table_temp_data_cleaning, temp)
#         table_temp = temp_sensor.result();

#     # appending the data
#     data['air_humi'].append(air_humi); data['air_temp'].append(air_temp); data['table_temp'].append(table_temp);

    
#     ## Assigning nan to the pressure 
#     pressure = float("nan");
#     ## Appending the pressure sensor to the data 
#     data['pressure'].append(pressure);
#     ## Appending time to the data
#     alpha = str(now - start);# aplha =str(alpha)
#     data['time'].append(alpha);
        

#     # Appending the data to the list
#     sensor_res.append(excel_time); sensor_res.append(air_humi); sensor_res.append(air_temp); sensor_res.append(table_temp); sensor_res.append(pressure); 
#     # print(i)
#     ## Creating the list for the sensor 
#     lst.append(sensor_res);

# print(lst)
# df = pd.DataFrame(lst, columns = data.keys())
# print(df)
# df.to_csv('IDK.csv', index=False)
# plt.show();