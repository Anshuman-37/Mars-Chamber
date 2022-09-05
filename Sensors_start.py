# ## Starting to write the code for the sensors
# import serial
# from serial.tools import list_ports
# port = list(list_ports.comports())
# for p in port:
#     print(p);
#     print(type(p.device)); print(p.name); print(p.serial_number); print(p.interface);

# ser = serial.Serial(p.device)
# print(ser.name)

import json
import subprocess
system_profile_data = subprocess.Popen(
    ['system_profiler', '-json', 'SPHardwareDataType'], stdout=subprocess.PIPE)
data = json.loads(system_profile_data.stdout.read())
serial = data.get('SPHardwareDataType', {})[0].get('serial_number')
print(serial)


# import serial

# serial_speed = 9600
# serial_port = 'P1610065'
# ser = serial.Serial(serial_port, serial_speed, timeout = 1)
# while True:
#     data = ser.readline()
#     if data: print(data); 


