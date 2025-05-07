import pandas as pd
import numpy as np
from prepare import prepare


df_cons = pd.read_csv("NGA-2015/cons_agg_wave3_visit1.csv")
df_durables = pd.read_csv("NGA-2015/sect5_plantingw3.csv")
#need to standardize column names to match 2018
df_durables.rename(columns={'s5q1': 'q_durable', 's5q4': 'resale_durable'}, inplace=True)
df_durables.to_csv("NGA-2015/edited_durables_file.csv", index=False)


df_cons['popw']  = df_cons["hhweight"] * df_cons["hhsize"]
df_cons.to_csv("NGA-2015/edited_cons_file.csv", index=False)

file_durables = "NGA-2015/edited_durables_file.csv"
file_cons = "NGA-2015/edited_cons_file.csv"

df = prepare(2015, "NGA", file_durables, file_cons)
#filtered_df = f[f['item_cd'] == 317]
#filtered_df = filtered_df[filtered_df['s5q1'] > 0]
#print(filtered_df)