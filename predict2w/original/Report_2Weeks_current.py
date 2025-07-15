import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# Importing data
folder_path = ""
file_name = "current_all_202507041338.csv"
Date_shift = -60

#%% # Data preprocessing
Data = pd.read_csv(folder_path+file_name)
N = len(Data['date'])

date_format_1 = '%Y-%m-%d %H:%M:%S'
date_format_2 = '%Y_%m_%d_%H_%M_%S'
Date = [datetime.datetime.strptime(x, date_format_1)-datetime.timedelta(days = Date_shift) for x in Data['date']]
Data['date'] = Date

Date_cut = datetime.datetime.strptime('2024_03_15_00_00_00', date_format_2)
Data = Data[Data['date'].tolist().index(Data['date'][Data['date']>Date_cut].tolist()[1]):]
Data.reset_index(drop=True, inplace=True)
print(Data["date"][0])
Start_date = datetime.datetime.strptime('2024_04_19_00_00_00', date_format_2)

import statistics as st
import numpy as np
import time
import math

#%% # Functions
def Prediction_approximation(Date, Data, Type, Interval, Method = None, img_name = None):
    
    Data = Data[Type]
    
    if Interval!='All':
        if Interval == 'Month':
            Interval = datetime.timedelta(days = 30)
            Title_2 = 'Месячный интервал'
        elif Interval == '2Weeks':
            Interval = datetime.timedelta(days = 14)
            Title_2 = 'Двухнедельный интервал'
        elif Interval == 'Week':
            Interval = datetime.timedelta(days = 7)
            Title_2 = 'Недельный интервал'
        
        Start_date = datetime.datetime.now() - Interval

        Data = Data[Date>Start_date]
        Date = Date[Date>Start_date]
        
        Data = Data[Date<datetime.datetime.now()]
        Date = Date[Date<datetime.datetime.now()]
        
        Data.reset_index(drop=True, inplace=True)
    else:
        Title_2 = 'Весь участок записи'
    
    Date = Date.tolist()
    
    if Method is not None:
        Date, Data = Filtering_processing(Date, Data, Method)
        print(Data)

        
    if Type == 'hodograph':
        Limit = [0.5, 0.8]
        Ylim = [0, 1]
        Ylabel = 'Эксцентриситет эллипса'
        Title_1 = 'Эллиптичность годографа тока'
        
    if Type == 'harmonics_a':
        Limit = [0.2, 0.1]
        Ylim = [0, 2]
        Ylabel = 'log_{10}(Сила тока, А)'
        Title_1 = 'Амплитуда кратных гармоник (фаза А) '

    if Type == 'harmonics_b':
        Limit = [0.2, 0.1]
        Ylim = [0, 2]
        Ylabel = 'log_{10}(Сила тока, А)'
        Title_1 = 'Амплитуда кратных гармоник (фаза B) '

    if Type == 'harmonics_c':
        Limit = [0.2, 0.1]
        Ylim = [0, 2]
        Ylabel = 'log_{10}(Сила тока, А)'
        Title_1 = 'Амплитуда кратных гармоник (фаза C) '

    if Type == 'slot_harmonics_a':
        Limit = [2.5, 2]
        Ylim = [2, 5]
        Ylabel = 'log_{10}(Сила тока, А)'
        Title_1 = 'Амплитуда пазовых гармоник (фаза А) '

    if Type == 'slot_harmonics_b':
        Limit = [2.5, 2]
        Ylim = [2, 5]
        Ylabel = 'log_{10}(Сила тока, А)'
        Title_1 = 'Амплитуда пазовых гармоник (фаза B) '

    if Type == 'slot_harmonics_c':
        Limit = [2.5, 2]
        Ylim = [2, 5]
        Ylabel = 'log_{10}(Сила тока, А)'
        Title_1 = 'Амплитуда пазовых гармоник (фаза C) '

    if Type == 'bar_harmonics':
        Limit = [1, 0.8]
        Ylim = [0, 3]
        Ylabel = 'log_{10}(Сила тока, А)'
        Title_1 = 'Амплитуда роторных гармоник '
    
    Time = []
    for i in range(len(Date)):
        Time.append(time.mktime(Date[i].timetuple()) + Date[i].microsecond / 1E6)
        if math.isnan(Data[i]):
            if i==len(Date)-1:
                Time = Time[:i]
                Data = Data[:i]
            else:
                Data[i] = Data[i+1]
                
    Start_time = Time[0]
    Time = [x - Start_time for x in Time]
    
    p = np.polyfit(Time,Data, 1)
    Data_app = np.polyval(p, Time)

    Defect_time = [(x-p[1])/p[0]+Start_time for x in Limit]
    try:
        Defect_date = [datetime.datetime.fromtimestamp(round(x)) for x in Defect_time]
        Defect_date = [x.strftime('%Y-%m-%d %H:%M:%S') if x>Date[0] else 'inf' for x in Defect_date]
    except:
        Defect_date = ['inf', 'inf']
    
    plt.figure(figsize=(8, 6))
    plt.scatter(Date, Data, color='blue')
    plt.plot(Date, Data_app, color='red')
    plt.title(Title_1 + ' (' + Title_2 + ')')
    plt.xlabel('Дата')
    plt.ylabel(Ylabel)
    plt.ylim(Ylim)
    plt.grid(True)
    plt.legend(['Статистические данные', 'Аппроксимация'], loc='upper right')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    
    if img_name is not None:
        plt.savefig(img_name)
        plt.close()
    else:
        plt.show()
        
    return Defect_date
    

def Filtering_processing(Date, Data, Method):
    
    Day, Data_filtered = [], []
    i = 0
    while i < len(Date)-1:
        Day_temp = Date[i]
        Data_filtered_temp = [Data[i]]
        k = 1
        while (i+k < len(Date)-1) and (Date[i+k].day == Day_temp.day):
            
            Data_filtered_temp.append(Data[i+k])
            k+=1
        
        Day.append(Day_temp)
        if Method == 'Mean':
            Data_filtered.append(st.mean(Data_filtered_temp))
        elif Method == 'Median':
            Data_filtered.append(st.median(Data_filtered_temp))
        elif Method == 'Min':
            Data_filtered.append(min(Data_filtered_temp))
        elif Method == 'Max':
            Data_filtered.append(max(Data_filtered_temp))
        
        i += k
        
    return Day, Data_filtered

#%% # Graphs to plot

(ellipse_ncrit_s, ellipse_crit_s) = Prediction_approximation(Data['date'], Data, 'hodograph', '2Weeks')
(ellipse_ncrit_l, ellipse_crit_l) = Prediction_approximation(Data['date'], Data, 'hodograph', 'All', 'Min')



