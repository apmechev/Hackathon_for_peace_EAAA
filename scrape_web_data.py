from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import string

#Todo: scrape all wepages from the complete website

#get text content from soup box
def content_stripper(box):
    list = []
    for l in box:
        list.append(l.text.strip())
    return list


#this function is for a single webpage
def scrape_single_page(web_page):

    #get html in soup object
    url = requests.get(web_page)
    htmltext = url.text
    soup = BeautifulSoup(htmltext,'html.parser')
    #get full language names, short language names & country
    country_box = soup.find("h1", attrs={'class':'title', 'id':'page-title'})
    full_lang_box = soup.find_all("div", attrs={'class':'title'})
    lang_box = soup.find_all("a", attrs={'href':re.compile('\/language\/')})

    full_lang_list = content_stripper(full_lang_box)
    lang_list = content_stripper(lang_box)
    lang_list = list(filter(re.compile('\[(\w{3})\]').match,lang_list))
    #remove brackets
    for i, l in enumerate(lang_list):
        lang_list[i] = l[1:-1]

    country_name = country_box.text.strip() # strip() is used to remove starting and trailing
    return country_name, lang_list, full_lang_list


def gen_letter_pairs():
    l = string.ascii_uppercase
    return ['{}{}'.format(l[i],l[j]) for i in range(len(l)) \
            for j in range(i + 1, len(l))]

pairs = gen_letter_pairs()
i = 0
df = pd.DataFrame(columns=['country', 'languages', 'full_languages'])

for p in pairs:
    web_page = 'https://www.ethnologue.com/country/{}/languages'.format(p)
    try:
        c, l, fl = scrape_single_page(web_page)
        if c!='{} not recognized'.format(p):
            df.loc[i] = [c, l, fl]
            i+=1
    except:
        print('No webpage found for 2 letter countrycode:{}'.format(p))

df.info()
df.to_csv('country_with_lang.csv')
print('debug')