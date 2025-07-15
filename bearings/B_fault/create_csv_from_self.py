import csv
from pathlib import Path

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

INPUT_DIR = "raw_self_data/defect"
OUTPUT_DIR = "csv_self_data/defect"


def save_to_csv(filename, values):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['vibration']) 
        for value in values:
            writer.writerow([value])


for file in Path(INPUT_DIR).iterdir():
    if file.is_file():
        header, data = extract_data(file)
        file_name = file.name.split(".")[:-1][0]
        save_to_csv(str(OUTPUT_DIR) + "/" + file_name + ".csv", data)

