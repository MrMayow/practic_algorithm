import scipy.io
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd

def extract_data(file_path):
    header = []
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line == "Data as Time Sequence:":
                break
            if line:  
                header.append(line)
        
        for line in file:
            line = line.strip()
            if line:  
                try:
                    value = float(line)
                    data.append(value)
                except ValueError:
                    continue  
    
    return header, data

file_path = 'data/Bearing_4/Defect/30Hz_accelerometer.txt'
header, data = extract_data(file_path)

print("Заголовок файла:")
for line in header:
    print(line)


print("\nПервые 10 значений данных:")
print(data[:10])

print(f"\nВсего значений данных: {len(data)}")