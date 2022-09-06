from gettext import install
from socket import timeout
import serial
from serial.tools import list_ports
import re;
import minimalmodbus as mm

class temp_sensor:
    '''Class to hold values for the temp sensor'''
    def __init__(self):
        '''Initialization of the class object'''
        self.port = 'NULL';
    
    def set_comp_port(self,comport):
        '''
        Params - Self reference, Comport number#
        Result - Set the value of the comport
        '''
        self.port = comport;
    
    def get_comp_port(self):
        '''
        Params - Self Reference 
        Result - Returns the stored comport
        '''
        return self.port;
    
    def set_sensors_values(self,sensor_data):
        '''
        Params - Self reference, Data obtained from the sensor
        Result - Retains the sensor data for temperatue 
        '''
        self.temperature_val = sensor_data
    
    def return_sensors_values(self):
        '''
        Params - Self Reference
        Result - Returns the value 
        '''
        return self.temperature_val; 

class humi_temp_sensors:
    '''Class to hold all the values for the humi sensor'''
    def __init__(self):
        '''Initialization of the class object'''
        self.port = 'NULL';
    
    def set_comp_port(self,comport):
        '''
        Params - Self reference, Comport number#
        Result - Set the value of the comport
        '''
        self.port = comport;

    def get_comp_port(self):
        '''
        Params - Self Reference 
        Result - Returns the stored comport
        '''
        return self.port;

    def set_sensors_values(self,sensor_data):
        '''
        Params - Self reference, Data obtained from the sensor in bytes format
        Result - Retains the sensor data for humidity and pressure
        '''
        self.sensor_data = str(sensor_data);
        self.humidity_val, self.temperature_val = self.sensor_data.split(' ')[1],self.sensor_data.split(' ')[4];
    
    def return_sensors_values(self):
        '''
        Params - Self Reference
        Result - Retains the value 
        '''
        return self.humidity_val,self.temperature_val; 

class sensors:
    '''Class to hold values for all the sensors'''
    def __init__(self):
        '''Initialzation of the class object'''
        self.humi_temp_sensor = humi_temp_sensors();
        self.temp_sensor = temp_sensor();

    def set_sensors_port(self,ports):
        '''
        Params - Self Reference, List of connected ports
        Result - Will set the port number of sensor by selecting the vendor
        '''
        # Declaring the regex for Vaisala 
        humi_temp_regex = re.compile(r'Vaisala');
        # Declaring the regex value for Temperature 
        temp_regex = re.compile(r'AU{1}'); 
        # Traversing over the list of ports
        for p in ports:
            # Searching for the Vaisala port 
            if(humi_temp_regex.search(p.description)):
                ## If found then set the port for humi_sensors
                self.humi_temp_sensor.set_comp_port(p.device);
            # Search for manufaturer for the temperatur sensor
            if(temp_regex.search(p.hwid)):
                ## If found then set the port for the temperature sensors
                self.temp_sensor.set_comp_port(p.device);

    def set_sensor_data(self):
        '''
        Params - Self Reference
        Result - Obtain the data for the sensors and set then to their respective objects 
        '''
        try:
            ## Open Connection for humi_sensor 
            ser = serial.Serial(self.humi_temp_sensor.get_comp_port(),baudrate=19200); ser.close(); ser.open();
            ## Command to recieve the data 
            data = 'send'; data += "\r\n";
            ## Send the command and obtain the result
            ser.write(data.encode()); obtained_data = ser.readline();
            ## Set the sensor values for the object of humi_temp_sensor 
            self.humi_temp_sensor.set_sensors_values(obtained_data);
            ## Close the connection
            ser.close();
        except:
            print('Humi Sensor not Present') 
        try:
            ## Open communication for the temperature sensor
            inst = mm.Instrument(self.temp_sensor.get_comp_port(),1);
            ## Setting up the variables for the instuction register
            inst.serial.baudrate = 9600 ; inst.serial.bytesize = 8;
            inst.serial.stopbits = 1; inst.serial.timeout = 1; inst.mode = mm.MODE_RTU; 
            ## Reading the value from the register
            temp = inst.read_register(0x1,1);
            ## Set the sensor value 
            self.temp_sensor.set_sensors_values(temp);
        except:
            print('Temp Sensor not present')

    def return_sensor_data(self):
        '''
        Params - Self Reference
        Result - Returns the data for the sensor object
        ''' 
        return self.humi_temp_sensor,self.temp_sensor; 

## Obtaining all the ports 
port = list(list_ports.comports())
# ## Creating a sensors object
# s = sensors(); 
# ## Setting the sensors port 
# s.set_sensors_port(port);
# ## Setting the sensor values
# s.set_sensor_data();
# ## Printing the data for the sensors 
# humi,temp = s.return_sensor_data()
# print('Sensor values for Vaisala', humi.return_sensors_values());
# print('Sensor Value for Simex Temp',temp.return_sensors_values());

pressure_regex = re.compile(r'FT{1}')
x = 'COM9' 
for p in port:
    print(p.__dict__)
    if(pressure_regex.search(p.hwid)):
        x = p.device;
    
while(1):
    ser = serial.Serial(x,baudrate=115200,timeout=1); ser.close(); ser.open();
    # data = 'vac?'; #data += "\r\n";
    # ser.write(data.encode());
    obtained_data = ser.readline();
    print(obtained_data); 
    ser.close();
    print('Reached the end ')





