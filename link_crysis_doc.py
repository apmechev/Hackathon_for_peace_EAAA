from get_disaster_data import *
import pandas as pd

APP_NAME= 'EA4'

LATEST_EVENTS = "https://api.reliefweb.int/v1/disasters?appname={}&preset=latest".format(APP_NAME)

crysis_data = get_n_latest_events_data()
df_crysis = pd.DataFrame(crysis_data)


csvdf = pd.read_csv('countrycodes.csv')
print(csvdf.head())
alpha2_trsl = {}
alpha3_trsl = {}
alpha3to2 = {}
for index, row in csvdf.iterrows():
    alpha2_trsl[row['CountryName']]=row["Alpha2Code"]
    alpha2_trsl[row['CountryName']]=row["Alpha3Code"]
    alpha3to2[row["Alpha3Code"].strip().rstrip()] = row["Alpha2Code"]

convert_dict = pd.Series(csvdf.Alpha3Code.values,index=csvdf.Alpha2Code).to_dict()

key_error_list = []
for iso3_list in df_crysis['iso3_codes']:
        iso2_list = []
        for code in iso3_list:
            try:
                iso2_list.append(convert_dict[code.strip().rstrip()])
            except:
                print('iso3code:', code, 'not found')
                key_error_list.append(code)
print('debug')