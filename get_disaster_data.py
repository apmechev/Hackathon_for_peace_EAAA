import requests
import json
APP_NAME= 'EA4'

LATEST_EVENTS = "https://api.reliefweb.int/v1/disasters?appname={}&preset=latest".format(APP_NAME)



def get_n_latest(n=20):
    r = requests.get("{}&limit={}".format(LATEST_EVENTS,n))
    if not r.ok:
        raise Exception(r.json())
    event_links=[i.get('href') for i in r.json().get('data')]
    return event_links


def get_country(event_json): 
    countries=[] 
    for data in event_json.get('data'): 
        for country in  data.get('fields').get('country'):  
            countries.append(country.get('name'))  
    return countries 
                                                         
def get_country_codes(event_json):
    codes=[]
    for data in event_json.get('data'):
        for country in  data.get('fields').get('country'):
            codes.append(country.get('iso3'))
    return codes


def get_name(event_json): 
    event_json.get('data')[0].get('fields').get('name')                                                      


def get_country(event_json):
    countries=[]
    for data in event_json.get('data'):
        for country in  data.get('fields').get('country'):
            countries.append(country.get('name'))
    return countries
                                                                                                             

def get_name(event_json): 
    return event_json.get('data')[0].get('fields').get('name') 
                                                                                                             

def get_description(event_json): 
    return event_json.get('data')[0].get('fields').get('description') 
                                                                                                             

def get_status(event_json): 
    return event_json.get('data')[0].get('fields').get('status') 
                                                                                                             

def get_date(event_json): 
    dates = list(event_json.get('data')[0].get('fields').get('date').keys()) 
    return event_json.get('data')[0].get('fields').get('date').get(dates[0]) 

def get_locations(event_json): 
    locations=[] 
    for data in event_json.get('data'): 
        for country in  data.get('fields').get('country'):  
            locations.append(country.get('location'))  
    return locations 
     
                                                                                                             

def get_event_type(event_json): 
    return event_json.get('data')[0].get('fields').get('type')[0] 
                                                                                                             

def get_event_current(event_json): 
    return event_json.get('data')[0].get('fields').get('curent') 
     
                                                                                                             

def get_event_id(event_json): 
    return event_json.get('data')[0].get('fields').get('id') 

def get_event_data(event_href):
    r = requests.get(event_href)
    if not r.ok:
        raise Exception(r.json())
    event_json = r.json()
    event_data={}
    event_data['countries']=get_country(event_json)
    event_data['iso3_codes']=get_country_codes(event_json)
    event_data['name']=get_name(event_json)
    event_data['description']=get_description(event_json)
    event_data['status']=get_status(event_json)
    event_data['date']=get_date(event_json)
    event_data['location']=get_locations(event_json)
    event_data['type']= get_event_type(event_json)
    event_data['current']=get_event_current(event_json)
    return event_data

def get_n_latest_events_data(n=10):
    events=[]
    for event in get_n_latest(n):
        events.append(get_event_data(event))
    return events


