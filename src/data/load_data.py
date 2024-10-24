import pandas as pd

file_path = '../../data/lectures_horaries_ABD.parquet'

df = pd.read_parquet(file_path)
print(df.head()) 
