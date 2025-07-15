import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import csv

file_name = "current_all_202507041338.csv"

Date_shift = -60

Data = pd.read_csv(file_name)

N = len(Data['date'])

date_format_1 = '%Y-%m-%d %H:%M:%S'
date_format_2 = '%Y_%m_%d_%H_%M_%S'

Date = [datetime.datetime.strptime(x, date_format_1)-datetime.timedelta(days = Date_shift) for x in Data['date']]
Data['date'] = Date

Date_cut = datetime.datetime.strptime('2024_03_15_00_00_00', date_format_2)
Data = Data[Data['date'].tolist().index(Data['date'][Data['date']>Date_cut].tolist()[1]):]
Data.reset_index(drop=True, inplace=True)

label = "hodograph"
dates = Data["date"]
values = Data[label]


def save_to_csv(filename, dates, values):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['date','value']) 
        for i in range(len(dates)):
            writer.writerow([dates[i], values[i]])

save_to_csv('dataset_hodograph.csv', dates, values)

