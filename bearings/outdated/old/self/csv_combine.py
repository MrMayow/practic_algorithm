import pandas as pd

files = ['bearing4_defect.csv', 'bearing4_nodefect.csv']

dfs = [pd.read_csv(f) for f in files]

combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_csv('bearing4_data.csv', index=False)

print(f"Объединено {len(files)} файлов в 'combined.csv'")
