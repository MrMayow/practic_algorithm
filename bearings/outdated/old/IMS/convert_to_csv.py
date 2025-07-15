import numpy as np
import csv

# Имя файла
filename = 'set1/2003.10.22.12.06.24'

# Чтение строк из файла
with open(filename, 'r') as f:
    lines = [line.strip() for line in f if line.strip()]

# Преобразование строк в числовой массив
matrix = [list(map(float, line.split())) for line in lines]
arr = np.array(matrix)

# Извлечение нужных столбцов (индексация с 0)
arr1 = arr[:, 1]  # 1-й столбец
arr3 = arr[:, 3]  # 3-й столбец
arr5 = arr[:, 5]  # 5-й столбец
arr7 = arr[:, 7]  # 7-й столбец

# Пример вывода первых 5 значений каждого массива
print('arr1:', arr1[:5])
print('arr3:', arr3[:5])
print('arr5:', arr5[:5])
print('arr7:', arr7[:5])

def save_to_csv(filename, values, header):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([header]) 
        for value in values:
            writer.writerow([value])

save_to_csv("NO_3.csv", arr5, "vibration")
save_to_csv("NO_4.csv", arr7, "vibration")
