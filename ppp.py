import pandas as pd

df = pd.read_csv("data/ppp/pwt1001.csv")


# For PPP at the year of the survey. Assume cell phones are consumption goods
def purchasing_power_parity(base_year, current_year, countrycode):  
    base_row = df[(df['year'] == base_year) & (df['countrycode'] == countrycode)]
    ppp = base_row["pl_c"]
    #For constant 2017 prices
    current_row = df[(df['year'] == current_year) & (df['countrycode'] == countrycode)]
    cgdpe = current_row["cgdpe"]
    rgdpna = base_row["rgdpna"]
    gdp_deflator = cgdpe.values[0] / rgdpna.values[0]

    return ppp.values[0], cgdpe.values[0], rgdpna.values[0], gdp_deflator



    '''preserve
	  use "${data}\ppp\pwt1001.dta", clear
	  *For PPP at the year of the survey. Assume cell phones are consumption goods
	  summ pl_c if countrycode == "`country'" & year == `baseyear'
	  local ppp`baseyear' = r(mean)
	  *For constant 2017 prices
	  summ cgdpe if countrycode == "`country'" & year == `currentyear'
	  local cgdpe_`currentyear' = r(mean)
	  summ rgdpna if countrycode == "`country'" & year == `baseyear'
	  local rgdpna_`baseyear' = r(mean)
	  local gdp_deflator_`baseyear' = (`cgdpe_`currentyear''/`rgdpna_`baseyear'')
    restore'''


#print(purchasing_power_parity(1970, "ABW"))

