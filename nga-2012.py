import pandas as pd
import numpy as np
from prepare import prepare
mapping_of_durables = {322: "Radio", 327: "TV", 320: "Generator", 332: "Smartphone", 317: "Bicycle", 319: "Car", 312: "Fridge", 318: "Motorbike"}

df_5a = pd.read_csv("NGA-2012/sect5a_plantingw2.csv")
df_5b = pd.read_csv("NGA-2012/sect5b_plantingw2.csv")

df_merged = pd.merge(df_5a, df_5b, on=['hhid','item_cd'], how='left', indicator=True)
#df_merged = df_merged[df_merged['_merge'] == 'both'] # if _merge == 3 
#df_merged.drop(columns=['_merge'], inplace=True) 

df_merged = df_merged[df_merged['s5q1'] != 0]
df_merged['obs_count'] = df_merged.groupby(['hhid', 'item_cd'])['hhid'].transform('count')
df_merged['mismatch'] = (df_merged['obs_count'] != df_merged['s5q1']).astype(int)



#filtered = df_merged[df_merged['tagDobs_phn'] == 1]

# Compute the median of s5q4 per hhid, only from filtered rows
#median_vals = filtered.groupby('hhid')['s5q4'].median()

# Map those medians back to the original dataframe
#df_merged['input_rv'] = df_merged['hhid'].map(median_vals)


#export to file 
df_merged.to_csv("NGA-2012/edited_planting_file.csv", index=False)

mismatch = df_merged[df_merged['mismatch'] == 1]
mismatch.to_csv("NGA-2012/mismatch.csv", index=False)



#consumption file 
df_cons = pd.read_csv("NGA-2012/cons_agg_wave2_visit1.csv")
#need to standardize column names to match 2018
df_cons['popw']  = df_cons["hhweight"] * df_cons["hhsize"]
df_cons.rename(columns={'totcons': 'totcons_adj_norm'}, inplace=True)

#export to file 
df_cons.to_csv("NGA-2015/edited_cons_file.csv", index=False)

file_durables = "NGA-2015/sect5_plantingw3.csv"
file_cons = "NGA-2015/edited_cons_file.csv"

#f = prepare(2015, "NGA", file_durables, file_cons)
#filtered_df = f[f['item_cd'] == 317]
#filtered_df = filtered_df[filtered_df['s5q1'] > 0]
#print(filtered_df)
#print(filtered_df['resale_durable'])
#print(filtered_df['s5q4']

