from bs4 import BeautifulSoup
import pandas as pd
import requests
import re


#Todo: scrape all wepages from the complete website

#this script is for a single webpage
web_page = 'https://www.ethnologue.com/country/EG/languages'

#get html in soup object
url = requests.get(web_page)
htmltext = url.text
soup = BeautifulSoup(htmltext,'html.parser')

#get text content from soup box
def content_stripper(box):
    list = []
    for l in box:
        list.append(l.text.strip())
    return list

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
df = pd.DataFrame(columns=['country','languages','full_languages'])
df.loc[0] = [country_name, lang_list, full_lang_list]
print(df)
