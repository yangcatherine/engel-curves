import pandas as pd

df = pd.read_csv("data/ppp/pwt1001.csv")


# For PPP at the year of the survey. Assume cell phones are consumption goods
def purchasing_power_parity(year, countrycode):  
    row = df[(df['year'] == year) & (df['countrycode'] == countrycode)]
    ppp = row["pl_c"]
    #For constant 2017 prices
    cgdpe = row["cgdpe"]
    rgdpna = row["rgdpna"]
    gdp_deflator = cgdpe / rgdpna

    return ppp, cgdpe, rgdpna, gdp_deflator



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


print(purchasing_power_parity(1970, "ABW"))

