from get_disaster_data import *


APP_NAME= 'EA4'

LATEST_EVENTS = "https://api.reliefweb.int/v1/disasters?appname={}&preset=latest".format(APP_NAME)

data = get_n_latest_events_data()

print('debug')