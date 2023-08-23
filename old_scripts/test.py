import pandas as pd


df = pd.read_csv(r'C:\Users\kenyo\shorelineAnalysis\after_drop_26.csv')

df = df.interpolate(method='linear')

df.to_csv('after_interpolate_26.csv')


