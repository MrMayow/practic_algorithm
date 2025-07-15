import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend

# Пути к файлам
names = ['data/Bearing_5/Defect/40Hz_accelerometer.txt']
legend_labels = ['Бороздка на внешнем кольце']
# legend_labels = ['Дефект ролика']
# legend_labels = ['Исправный подшипник']

# Коэффициенты пересчёта
coef = 1000. / np.array([2.01, 1.99, 10.34, 10.2337])

n_signals = len(names)
N_list = []
Fs_list = []
T_list = []

# Считывание заголовков
for name in names:
    header_length = 19
    with open(name, 'r') as f:
        header = [next(f).strip() for _ in range(header_length)]

    N = int(header[2][18:])  # строка 3, с 19-го символа
    Fs = float(header[7][19:]) * 1e3  # строка 8, с 20-го символа
    T = float(header[8][19:])  # строка 9, с 20-го символа

    N_list.append(N)
    Fs_list.append(Fs)
    T_list.append(T)

max_N = max(N_list)
max_T = max(T_list)
Fs = max(Fs_list)
Time = np.linspace(0, max_T, max_N)
Data = np.zeros((max_N, n_signals))

# Считывание сигналов
for i, name in enumerate(names):
    header_length = 19
    with open(name, 'r') as f:
        header = [next(f).strip() for _ in range(header_length)]
        data = np.loadtxt(f)
    scaled_data = data * coef[i]

    if max_N == min(N_list):
        Data[:, i] = detrend(scaled_data)
    else:
        t_orig = np.linspace(0, float(header[8][19:]), N_list[i])
        interp_data = np.interp(Time, t_orig, scaled_data)
        Data[:, i] = detrend(interp_data)

# Построение графика
plt.figure(figsize=(10, 4))
plt.plot(Time, Data)
plt.xlim([0.5, 1.5])
plt.xlabel('Время, с')
plt.ylabel('Ускорение, м/с²')
plt.title('Сигналы с акселерометра')
plt.legend(legend_labels)
plt.grid(True)
plt.tight_layout()
plt.savefig("plot.png", dpi=300)
