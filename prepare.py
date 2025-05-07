import pandas as pd
import numpy as np
from ppp import purchasing_power_parity


# Load dataset
#df_durables = pd.read_csv("NGA-2018/sect5_plantingw4.csv")
#df_cons = pd.read_csv("NGA-2018/totcons_final.csv") 
base_year = 2017
mapping_of_durables = {322: "Radio", 320: "Generator", 327: "TV", 332: "Smartphone", 317: "Bicycle", 319: "Car", 312: "Fridge", 318: "Motorbike"}
# ADD GENERATORS 
'''
Radio:			item_cd == 322
TV:				item_cd == 327
Smartphones:	item_cd == 3321
Bycicles:		item_cd == 317
Car:			item_cd == 319
Fridge:			item_cd == 312
Motorbike:		item_cd == 318'''

def prepare(current_year, countrycode, file_durables, file_cons): 
		df_durables = pd.read_csv(file_durables)
		df_cons = pd.read_csv(file_cons) 

		#get ppp 
		ppp, cgdpe, rgdpna, gdp_deflator = purchasing_power_parity(base_year, current_year, countrycode)
		
		r = 0.02 # interest rate 
		δ = 0.05 # physical depreciation rate
		o = 0.13 # induced obsolescence

		#keep only records for durables of interest
		durables_of_interest = [322, 327, 332, 317, 319, 312, 318, 320]
		df_durables = df_durables[df_durables['item_cd'].isin(durables_of_interest)]

		#number of durables
		#df_durables['k_durable'] = df_durables['s5q1'] #quantity of durables in household
		#type of consumer durable
		df_durables['durable'] = df_durables['item_cd']
		df_durables['durable'] = df_durables['item_cd'].map(mapping_of_durables)
		#Resale value of one of the durables in the hh
		#df_durables['resale_durable'] = df_durables['s5q4'] #RELABEL AS JUST RESALE_DURABLE***

		#merge with consumption data and keep only if households exist in both datasets
		merge_df = pd.merge(df_durables, df_cons, on='hhid', how='left', indicator=True) #merging on household id 
		merge_df = merge_df[merge_df['_merge'] == 'both']
		merge_df.drop(columns=['_merge'], inplace=True)
		
		#This dataset provides household level weights, note: wt_wave4*hhsize=popw, hhsize *hhweight = popw
		merge_df['q_durable_w'] = merge_df['q_durable'] * merge_df['popw']

		#total consumption variables and weights 
		merge_df['c_tot'] = merge_df['totcons'] * merge_df['hhsize']
		merge_df['c_tot_w'] = merge_df['c_tot'] * merge_df['popw']

		#replace consumption variables with ppp adjustments 
		merge_df['resale_durable'] = (merge_df['resale_durable'] / ppp) / gdp_deflator
		merge_df['c_tot'] = (merge_df['c_tot'] / ppp) / gdp_deflator
		merge_df['c_tot_w'] = (merge_df['c_tot_w'] / ppp) / gdp_deflator
		
		#Estimate user cost of capital 
		merge_df['usercost'] = merge_df['resale_durable'] * ((1+r)-(1-δ)*(1-o))
		merge_df['k_value'] = merge_df['usercost'] * merge_df['q_durable']
		#merge_df['k_value_w'] = merge_df['usercost'] * merge_df['k_durable_w']

		merge_df['lcons'] = np.log(merge_df['c_tot']/12) #by month -> double check monthly consumption 
		merge_df['lhhphresale'] = np.log(merge_df['resale_durable'])
		
		# generate dummies for household size: Indicator for HH size: 1 (<=2), 2 (3-4), 3 (>=5)"
		#merge_df['hhsizeindic'] = np.where(merge_df['hhsize'] <= 2, 1, np.nan)
		#merge_df['hhsizeindic'] = np.where((merge_df['hhsize'] >= 2) & (merge_df['hhsize'] >= 4), 2, np.nan)
		#merge_df['hhsizeindic'] = np.where(merge_df['hhsize'] >= 5, 3, np.nan)
		
		#share of durable in monthly consumption 
		merge_df["durable_sh"] = merge_df["k_value"] / (merge_df["c_tot"] / 12)

		#Find observations if value of durable expenses are above total consumption in the year (error!)
		errors = merge_df[(merge_df['k_value'] * 12 >= merge_df['c_tot']) & (merge_df['k_value'].notna())]
		print("*********************ERRORS**************************************")
		print(errors)
		print(ppp, cgdpe, rgdpna, gdp_deflator)

		#left at line 141 in stata

		return merge_df


#merge_df = prepare(2018, "NGA", "NGA-2018/sect5_plantingw4.csv", "NGA-2018/totcons_final.csv")
#print(merge_df)
  
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