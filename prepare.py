import pandas as pd
import numpy as np
from ppp import purchasing_power_parity

# Load dataset
df_durables = pd.read_csv("NGA-2018/sect5_plantingw4.csv")
df_cons = pd.read_csv("NGA-2018/totcons_final.csv") 
mapping_of_durables = {322: "Radio", 327: "TV", 3321: "Smartphones", 317: "Bicycles", 319: "Car", 312: "Fridge", 318: "Motorbike"}
'''
Radio:			item_cd == 322
TV:				item_cd == 327
Smartphones:	item_cd == 3321
Bycicles:		item_cd == 317
Car:			item_cd == 319
Fridge:			item_cd == 312
Motorbike:		item_cd == 318'''

def prepare(year, countrycode): 
		global df_durables, df_cons

		#get ppp 
		ppp, cgdpe, rgdpna, gdp_deflator = purchasing_power_parity(year, countrycode)
		
		r = 0.02 # interest rate 
		δ = 0.05 # physical depreciation rate
		o = 0.13 # induced obsolescence

		#keep only records for durables of interest
		durables_of_interest = [322, 327, 3321, 317, 319, 312, 318]
		df_durables = df_durables[df_durables['item_cd'].isin(durables_of_interest)]

		#number of durables
		df_durables['k_durable'] = df_durables['s5q1']
		#type of consumer durable
		df_durables['durable'] = df_durables['item_cd']
		df_durables['durable'] = df_durables['item_cd'].map(mapping_of_durables)
		#Resale value of one of the durables in the hh
		df_durables['resale_durable'] = df_durables['s5q4'] 

		#merge with consumption data and keep only if households exist in both datasets
		merge_df = pd.merge(df_durables, df_cons, on='hhid', how='left', indicator=True)
		merge_df = merge_df[merge_df['_merge'] == 'both']
		merge_df.drop(columns=['_merge'], inplace=True)
		
		#This dataset provides household level weights, note: wt_wave4*hhsize=popw
		merge_df['k_durable_w'] = merge_df['k_durable'] * merge_df['popw']

		#total consumption variables and weights 
		merge_df['c_tot'] = merge_df['totcons_adj_norm'] * merge_df['hhsize']
		merge_df['c_tot_w'] = merge_df['c_tot'] * merge_df['popw']

		#replace consumption variables with ppp adjustments 
		merge_df['resale_durable'] = (merge_df['resale_durable'] / ppp) / gdp_deflator
		merge_df['c_tot'] = (merge_df['c_tot'] / ppp) / gdp_deflator
		merge_df['c_tot_w'] = (merge_df['c_tot_w'] / ppp) / gdp_deflator
		
		#Estimate user cost of capital 
		merge_df['usercost'] = merge_df['resale_durable'] * ((1+r)-(1-δ)*(1-o))
		merge_df['k_value'] = merge_df['usercost'] * merge_df['k_durable']
		merge_df['k_value_w'] = merge_df['usercost'] * merge_df['k_durable_w']

		merge_df['lcons'] = np.log(merge_df['c_tot']/12)
		merge_df['lhhphresale'] = np.log(merge_df['resale_durable'])
		
		# generate dummies for household size: Indicator for HH size: 1 (<=2), 2 (3-4), 3 (>=5)"
		merge_df.loc[merge_df['hhsize'] <= 2, 'hhsizeindic'] = 1
		merge_df.loc[merge_df['hhsize'] <= 4 & merge_df['hhsize'] >= 2, 'hhsizeindic'] = 2
		merge_df.loc[merge_df['hhsize'] >= 5, 'hhsizeindic'] = 3
		
		#share of durable in monthly consumption 
		merge_df["durable_sh"] = merge_df["k_value"] / (merge_df["c_tot"] / 12)

		#Find observations if value of durable expenses are above total consumption in the year (error!)
		errors = merge_df[(merge_df['k_value'] * 12 >= merge_df['c_tot']) & (merge_df['k_value'].notna())]
		print("********ERRORS********************")
		print(errors)

		#left at line 141 in stata

		return merge_df


merge_df = prepare(2018, "NGA")
print(merge_df)
  
'''
*Estimate usercost of capital
gen usercost = resale_durable * ((1+`r')-(1-`δ')*(1-`o'))
gen k_value = usercost * k_durable
gen k_value_w = usercost * k_durable_w

gen lcons=log(c_tot/12)
gen lhhphresale = log(resale_durable)

*dummies for household size
gen hhsizeindic = 1 if hhsize<=2
replace hhsizeindic = 2 if hhsize>=3 & hhsize<=4
replace hhsizeindic = 3 if hhsize>=5
label var hhsizeindic "Indicator for HH size: 1 (<=2), 2 (3-4), 3 (>=5)"

*share of durable in monthly consumption
gen durable_sh = (k_value)/(c_tot/12)
label var durable_sh "share of durable in monthly consumption"

*Find if value of durable expenses are above total consumption in the year (error!)
list hhid durable if k_value *12 >= c_tot & k_value != . '''