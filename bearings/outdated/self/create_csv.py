import csv

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

ID = 'balldefect'
FILE_PATH = 'data/Bearing_2/30Hz_accelerometer.txt'
CSV_PATH = 'bearing2_balldefect.csv'
header, data = extract_data(FILE_PATH)


def save_to_csv(filename, values):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['vibration']) 

        for value in values:
            writer.writerow([value])

save_to_csv(CSV_PATH, data, ID)

print(f'CSV файл "{CSV_PATH}" успешно создан.')
