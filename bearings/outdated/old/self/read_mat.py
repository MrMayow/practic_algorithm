import scipy.io
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

Bearing_data = scipy.io.loadmat('./dataCWRU/ball.mat')
print(Bearing_data.keys())

vibration_signal_bearing = Bearing_data['X119_DE_time']
print(vibration_signal_bearing)
print(vibration_signal_bearing.shape)

sampling_rate = 12000  # 12 kHz
duration = 10 

time = np.arange(0, duration, 1/sampling_rate)
vibration_signal_bearing = vibration_signal_bearing[:len(time)]

plt.plot(time, vibration_signal_bearing)
plt.title('Vibration Signal vs Time(Bearing)')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.savefig("plot3.png", dpi=300)