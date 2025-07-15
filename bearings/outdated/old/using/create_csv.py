import scipy.io
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
import csv

ID = 'balldefect'
FILE_PATH = 'test_balldefect_2.mat'
CSV_PATH = 'balldefect_2.csv'

Bearing_data = scipy.io.loadmat(FILE_PATH)
print(Bearing_data.keys())

vibration_signal_bearing = Bearing_data['X108_FE_time']
print(vibration_signal_bearing)
print(len(vibration_signal_bearing))

def save_to_csv(filename, values, fixed_value):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['vibration', 'label']) 

        for value in values:
            writer.writerow([value[0], fixed_value])

save_to_csv(CSV_PATH, vibration_signal_bearing, ID)