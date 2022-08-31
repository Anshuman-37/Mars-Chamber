## import libraries




## Creating a class for the sensors 
class Sensor:
    ## Intializing the sensors
    def __init__(self):
        self.temp = None
        self.pressure = None
        self.light = None ## more like control 
        self.humidity = None 
    

    ## Setting the temperature Values
    def set_temperature(self):
        '''
        Params - Specific Temperature Values
        Result - Set temperature to specific value
        '''
        if(True): return 1;
        return 0;

    ## Setting the pressure values
    def set_pressure(self):
        '''
        Params - Specific Pressure Values
        Result - Set pressure sensor to specifc value
        '''
        if(True): return 1;
        return 0;

    ## Setting the light values 
    def set_light(self):
        '''
        Params - Light on and off 
        Result - Set the light to specific value
        '''
        if(True): return 1;
        return 0; 
    
    ## Modulating the humidity
    def modulate_humidity(self):
        '''
        Params - 
        Result - 
        '''
        if(self.temp and self.pressure): return 1;
        return 0;

    ## Add more member functions 

    
##