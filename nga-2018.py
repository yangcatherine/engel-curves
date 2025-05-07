import pandas as pd
import numpy as np
from prepare import prepare
from clean import clean


df_durables = pd.read_csv("NGA-2018/sect5_plantingw4.csv")
df_cons = pd.read_csv("NGA-2018/totcons_final.csv")

#need to standardize column names
df_durables.rename(columns={'s5q1': 'q_durable', 's5q4': 'resale_durable'}, inplace=True)
df_durables.loc[df_durables['item_cd'] == 3321, 'item_cd'] = 332
df_durables.to_csv("NGA-2018/edited_durables_file.csv", index=False)

df_cons.rename(columns={'totcons_pc': 'totcons'}, inplace=True)
df_cons.to_csv("NGA-2018/edited_cons_file.csv", index=False)

file_durables = "NGA-2018/edited_durables_file.csv"
file_cons = "NGA-2018/edited_cons_file.csv"

df = prepare(2018, "NGA", file_durables, file_cons)
#print(df)
#print(df['resale_durable'])
#print(df['s5q4'])
df.to_csv("NGA-2018/prepare.csv", index=False)
dropdf = df.drop_duplicates(subset='hhid', keep='first')
dropdf.to_csv("NGA-2018/drop.csv", index=False)

