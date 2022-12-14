## Import Files
import pandas as pd
import datetime

## Object Wrapper
class Day: 
    '''The class to store the date'''
    
    def __init__(self):
        '''Intiallize the date'''
        self.date = datetime.datetime(2021,7,3) ## My random birthday just to intialize
    
    def set_date(self,d):
        '''
        Params - Reference , date observed in excel file
        Result - Set the date for the class
        '''
        self.date = d
    
    def return_date(self):
        '''
            Params - Reference 
            Result - Returns the date for the object
        '''
        return self.date;
    
    def set_temperature(self,temperature):
        '''
            Params - Reference, temperature values 
            Result - Sets the temperature for the specific day
        '''
        self.temperature = temperature;
    
    def set_pressure(self,pressure):
        '''
            Params - Reference, pressure values 
            Result - Sets the pressure for the specific day
        '''
        self.pressure = pressure;
    
    def set_humidity(self,humidity):
        '''
            Params - Reference, humidity values 
            Result - Sets the humidity for the specific day
        '''
        self.humidity = humidity;
    
    def set_uv_light(self,uv_light):
        '''
            Params - Reference, uv_light values 
            Result - Sets the uv_light for the specific day
        '''
        self.uv_light = uv_light;
    
    def set_time(self,time):
        '''
            Params - Reference, time values 
            Result - Sets the time for the specific day and stores the integer value of time
        '''
        self.int_time = []
        self.time = time;
        # Iterating over time in datetime format to convert
        for i in time: self.int_time.append(int(i.strftime('%H'))); 
    
    def return_all(self):
        '''
            Params - Reference
            Result - Returns all the stored variables
        '''
        return self.time,self.int_time,self.temperature,self.pressure,self.humidity,self.uv_light
    
    def return_plot_data_temperature(self):
        '''
            Params - Reference 
            Result - Returns the integer time data and temperature 
        '''
        return self.int_time,self.temperature
    
    def return_plot_data_pressure(self):
        '''
            Params - Reference 
            Result - Returns the integer time data and pressure
        '''
        return self.int_time,self.pressure
    
    def return_plot_data_humidity(self):
        '''
            Params - Reference 
            Result - Returns the integer time data and humidity
        '''
        return self.int_time,self.humidity
    
    def return_plot_data_uv_light(self):
        '''
            Params - Reference 
            Result - Returns the integer time data and uv light
        '''
        return self.int_time,self.uv_light

def data_preprocessing(path):
    '''
        Params - The path of the data/excel file
        Result - Returns the object array for each specificied date in OOPS format
    '''
    ## Reading the data
    df = pd.read_excel(path); 
    ## Making the dates array 
    dates_array = []; all_dates = [];
    ## Key and Values data 
    for key, value in df.iteritems():
        ## Check the date key
        if key == 'Date':
            all_dates.append(value[0]);
            ## Checking how many dates are there 
            for i in range(1,len(value)):
                if value[i-1]!=value[i]: all_dates.append(value[i]); 
    
    ## Iterating over all dates 
    for i in all_dates:
        ## Setting the dates from the plot
        x = Day(); x.set_date(i); #print(x.return_date());
        ## Variables to store the values for the fields
        time = []; temp = []; pressure = []; humidity = []; uv_light = []; 
        ## Iterating over dataframe to obtain the values 
        for index, row in df.iterrows():
            ## If the date is same as stored in the object
            if i == row['Date']: 
                ## Appending the values to specific to store them
                time.append(row['Time']); temp.append(row['Temperature']);
                pressure.append(row['Pressure']); humidity.append(row['Humidity']); uv_light.append(row['UV light']);
        ## Set the time,temp,pressure,humidity and the uv_light for the class object
        x.set_time(time); x.set_temperature(temp); x.set_pressure(pressure); x.set_humidity(humidity); x.set_uv_light(uv_light);
        ## Creating an array of objects, each object refered to a specific date
        dates_array.append(x);
    ## Return the dates array 
    return dates_array
