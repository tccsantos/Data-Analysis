import pandas as pd
df = pd.read_csv('URL.csv', encoding='ANSI')
df.to_csv('URLgrande.csv', encoding= 'utf-8', index=False)