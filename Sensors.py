# ## import libraries




# ## Creating a class for the sensors 
# class Sensor:
#     ## Intializing the sensors
#     def __init__(self):
#         self.temp = None
#         self.pressure = None
#         self.light = None ## more like control 
#         self.humidity = None 
    

#     ## Setting the temperature Values
#     def set_temperature(self):
#         '''
#         Params - Specific Temperature Values
#         Result - Set temperature to specific value
#         '''
#         if(True): return 1;
#         return 0;

#     ## Setting the pressure values
#     def set_pressure(self):
#         '''
#         Params - Specific Pressure Values
#         Result - Set pressure sensor to specifc value
#         '''
#         if(True): return 1;
#         return 0;

#     ## Setting the light values 
#     def set_light(self):
#         '''
#         Params - Light on and off 
#         Result - Set the light to specific value
#         '''
#         if(True): return 1;
#         return 0; 
    
#     ## Modulating the humidity
#     def modulate_humidity(self):
#         '''
#         Params - 
#         Result - 
#         '''
#         if(self.temp and self.pressure): return 1;
#         return 0;

#     ## Add more member functions 
#%%
from datetime import datetime
from random import randint
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax = fig.add_subplot()

time_series = []
value_a_series = []
value_b_series = []

def generate_dummy_data():
    time = datetime.now()
    value_a = randint(-100, 100)
    value_b = randint(-10, 10)

    time_series.append(time)
    value_a_series.append(value_a)
    value_b_series.append(value_b)

def animate(i):

    generate_dummy_data()

ax.clear()

plt.title('An animated graph')
plt.xlabel('Time')
plt.ylabel('values')

ax.plot(time_series, value_a_series, label='value_a_series')
ax.plot(time_series, value_b_series, label='value_b_series')

plt.legend()
fig.autofmt_xdate()

ani = animation.FuncAnimation(fig,
                              animate,
                              interval=1000)

plt.show()
#%%
