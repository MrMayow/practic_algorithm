import pandas as pd

files = ['nodefect.csv', 'balldefect_2.csv']

dfs = [pd.read_csv(f) for f in files]

combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_csv('test_ball_defect_2.csv', index=False)

print(f"Объединено {len(files)} файлов в 'combined.csv'")
