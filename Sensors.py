## import libraries




## Creating a class for the sensors 
class Sensor:
    ## Intializing the sensors
    def __init__(self):
        self.temp = None
        self.pressure = None
        self.light = None
    

    ## Setting the temperature Values
    def set_temperature(self):
        if(True): return 1;
        return 0;

    ## Setting the pressure values
    def set_pressure(self):
        if(True): return 1;
        return 0;

    ## Setting the light values 
    def set_light(self):
        if(True): return 1;
        return 0; 
    
    ## Modulating the humidity
    def modulate_humidity(self):
        if(self.temp and self.pressure): return 1;
        return 0;

    ## Add more member functions 

    
##