import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# === Параметры ===
file_path = 'bearing1_nodefect.csv'      # Замените на путь к вашему файлу
column_name = 'vibration'     # Замените на имя столбца с данными
fs = 9000                       # Частота дискретизации, Гц (уточните для своих данных)
cutoff = 30                     # Частота среза фильтра, Гц (можно менять)

# === Загрузка данных ===
data = pd.read_csv(file_path)
acc = data[column_name].values
time = np.arange(len(acc)) / fs

# === Фильтрация: высокочастотный фильтр Баттерворта ===
order = 4  # порядок фильтра
b, a = butter(N=order, Wn=cutoff/(fs/2), btype='high')
acc_filtered = filtfilt(b, a, acc)

# === Построение графиков ===
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time, acc, label='Исходный сигнал')
plt.xlim([0.5, 1.5])
plt.xlabel('Время, с')
plt.ylabel('Ускорение, м/с²')
plt.title('Исходный сигнал')
plt.grid()
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time, acc_filtered, color='orange', label=f'После фильтрации (>{cutoff} Гц)')
plt.xlim([0.5, 1.5])
plt.xlabel('Время, с')
plt.ylabel('Ускорение, м/с²')
plt.title(f'Сигнал после удаления частот ниже {cutoff} Гц')
plt.grid()
plt.legend()

plt.tight_layout()
plt.savefig("filtered.png", dpi=300)
