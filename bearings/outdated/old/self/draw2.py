import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, windows
from scipy.ndimage import uniform_filter1d
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

# Расчёт FFT
N = Data.shape[0]
Freq = Fs * np.arange(0, N//2 + 1) / N
FFT_Data_full = np.fft.fft(Data, axis=0)
FFT_Data = 2.0 / N * np.abs(FFT_Data_full[:N//2 + 1, :])  # только положительные частоты

# Поиск пиков (на примере использования scipy)
Window = 10
Threshold = 0.5

class Peak:
    def __init__(self, Freq, Amp):
        self.Freq = Freq
        self.Amp = Amp

Peaks = []
start_idx = int(round(Time[-1]))  # округляем последний индекс времени

for i in range(Data.shape[1]):
    y = FFT_Data[start_idx:, i]
    x = Freq[start_idx:]
    peaks, _ = find_peaks(y, height=Threshold, distance=Window)
    for p in peaks:
        Peaks.append(Peak(Freq=start_idx + p, Amp=y[p]))

# Максимизация и сглаживание спектра
Window = 3
FFT_data_max = np.copy(FFT_Data)

for j in range(Data.shape[1]):
    for i in range(Window, (N//2 - Window)):
        FFT_data_max[i, j] = np.max(FFT_Data[i - Window:i + Window + 1, j])
    FFT_data_max[:, j] = uniform_filter1d(FFT_data_max[:, j], size=Window)

# Визуализация
plt.figure(figsize=(10, 4))
for j in range(Data.shape[1]):
    plt.plot(Freq, np.log10(FFT_data_max[:, j]), label=legend_labels[j])

for peak in Peaks:
    plt.plot(Freq[peak.Freq], np.log10(peak.Amp), '*', label='Peak')

plt.grid(True)
plt.xlim([0, Fs / 2])
plt.ylim([-2, 1.5])
plt.xlabel('Частота, Гц')
plt.ylabel(r'$\log_{10}$(Ускорение), м/с²')
plt.title('Частотный спектр сигналов с акселерометра')
plt.legend()
plt.tight_layout()
plt.savefig("plot2.png", dpi=300)
