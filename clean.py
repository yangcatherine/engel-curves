import pandas as pd
import numpy as np


def clean(df): 

    #drop duplicates because most hhs repeated because they have the two items being analyzed (not needed anymore because all durables in file)
    #df = df.drop_duplicates(subset='hhid', keep='first')

    #trim upper and lower 1% of sample in terms of consumption
    lower_percentile = df['lcons'].quantile(0.01)
    upper_percentile = df['lcons'].quantile(0.99)
    df['tagout1'] = np.where((df['lcons'] <= lower_percentile) | (df['lcons'] >= upper_percentile), 1, 0)
    outlier_cons = df[['hhid', 'tagout1']]

    #trim upper and lower 1% in terms of resale value of each durable
    df['tagout2'] = np.nan
    medians = {}
    for good in df['durable'].unique():
        good_df = df[df['durable'] == good]
        lower_percentile_resale = good_df['lhhphresale'].quantile(0.01)
        upper_percentile_resale = good_df['lhhphresale'].quantile(0.99)

    # get 1st and 99th percentiles for resale value
    lower_percentile_resale = good_df['lhhphresale'].quantile(0.01)
    upper_percentile_resale = good_df['lhhphresale'].quantile(0.99)
    
    # replace 'tagout2' for outliers
    df.loc[(df['durable'] == good) & ((df['lhhphresale'] <= lower_percentile_resale) | (df['lhhphresale'] >= upper_percentile_resale)), 'tagout2'] = 1
    
    outlier_res = df[['hhid', 'durable', 'tagout2']]

    #merging and trimming
    merge_df = pd.merge(df, outlier_cons, on='hhid', how='left')
    merge_df = pd.merge(merge_df, outlier_res, on=['hhid', 'durable'], how='left')
    print(merge_df)
    merge_df['outlier'] = np.where((merge_df['tagout1'] == 1) | (merge_df['tagout2'] == 1), 1, 0)
    clean_df = merge_df[merge_df['outlier'] != 1]

    return clean_df
