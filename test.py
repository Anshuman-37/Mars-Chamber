## Import Files
from gettext import install
from socket import timeout
import serial
from serial.tools import list_ports
import re;
import minimalmodbus as mm
import concurrent.futures
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
    
class pressure_sensor:
    '''Class to hold values for the presure sensor'''
    def __init__(self):
        '''Initialization of the class object'''
        self.port = 'NULL';
    
    def set_comp_port(self,comport):
        '''
        Params - Self reference, Comport number
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
        Result - Retains the sensor data for temperature
        '''
        self.pressure_val = sensor_data
    
    def return_sensors_values(self):
        '''
        Params - Self Reference
        Result - Returns the value 
        '''
        return self.pressure_val; 

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
        self.pressure_sensor = pressure_sensor();

    def interim_set_ports(self,ports,search_string,cntrl_val):
        '''
        Params - Self Reference, List of connected Ports , A string for Regex, Control Value for which sensor
        Result - Set the sensor ports accordingly 
        '''
        ## To serach the which sensor data we want to set
        search_reg = re.compile(r''+search_string);
        ## Traversing over ports
        for p in ports:
            ## For humidity sensor 
            if(search_reg.search(p.description) and cntrl_val == 0):
                self.humi_temp_sensor.set_comp_port(p.device);
            ## Temperature sensor
            if(search_reg.search(p.hwid) and cntrl_val == 1):
                self.temp_sensor.set_comp_port(p.device);
            ## Pressure Sensor 
            if(search_reg.search(p.hwid) and cntrl_val == 2):
                self.pressure_sensor.set_comp_port(p.device);
            
    def connect_humi_sensor(self):
        '''
        Params - Self Reference
        Result - Obtain the data for the humi sensor and set then to their respective objects 
        '''
        try:
            ## Open Connection for humi_sensor 
            ser = serial.Serial(self.humi_temp_sensor.get_comp_port(),baudrate=19200); ser.close(); ser.open();
            ## Command to recieve the data 
            data = 'send'; data += "\r\n";
            ## Send the command and obtain the result
            ser.write(data.encode()); obtained_data = ser.readline(); ser.write(data.encode()); obtained_data = ser.readline()
            ## Set the sensor values for the object of humi_temp_sensor 
            self.humi_temp_sensor.set_sensors_values(obtained_data);
            ## Close the connection
            ser.close();
        except:
            print('Humi Sensor not Present')

    def connect_table_temp_sensor(self):
        '''
        Params - Self Reference
        Result - Obtain the data for the table temp sensor and set then to their respective objects 
        '''
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
    
    def set_sensors_port(self,ports):
        '''
        Params - Self Reference, List of connected ports
        Result - Will set the port number of sensor by selecting the vendor
        '''
        ## Multithreading to set sensor ports
        with concurrent.futures.ThreadPoolExecutor() as exe:
            humi_sensor = exe.submit(self.interim_set_ports,ports,'Vaisala',cntrl_val = 0); #humi_sensor.result();
            temp_sensor = exe.submit(self.interim_set_ports,ports,'AU{1}',cntrl_val = 1); #temp_sensor.result();
            pres_sensor = exe.submit(self.interim_set_ports,ports,'FT{1}',cntrl_val = 2); #pres_sensor +.result();
            humi_sensor.result(); temp_sensor.result(); pres_sensor.result();
    
    def set_sensor_data(self):
        '''
        Params - Self Reference
        Result - Obtain the data for the sensors and set then to their respective objects 
        '''
        ## Multithreading to set sensor data
        with concurrent.futures.ThreadPoolExecutor() as exe:
            humi_sensor = exe.submit(self.connect_humi_sensor);#  humi_sensor.result();
            temp_sensor = exe.submit(self.connect_table_temp_sensor); #+temp_sensor.result()
            humi_sensor.result(); temp_sensor.result();

        ## TODO Set the values for the pressure sensor 
        # try:
             
        # except:

    def return_sensor_data(self):
        '''
        Params - Self Reference
        Result - Returns the data for the sensor object
        ''' 
        ## TODO add pressure sensor as well once you obtain the values
        return self.humi_temp_sensor,self.temp_sensor; 