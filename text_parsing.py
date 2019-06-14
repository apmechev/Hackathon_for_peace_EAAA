from langdetect import detect 
import os
import xml.etree.ElementTree as ET
from langdetect.lang_detect_exception import LangDetectException      



def dictionary_count(text, dictionary={}): 
    """reads an XML element, gets the text, detects the  language
    using langdetect and puts it in the dictionary"""
    try:
        temp_lang=detect(text) 
    except LangDetectException:
        return dictionary
    if temp_lang in dictionary.keys(): 
        dictionary[temp_lang]+=1 
    else: 
        dictionary[temp_lang]=1 
    return dictionary 


def get_text_from_transunit(trans_unit, field):
    """Gets all the text in the translation unit tag, and concatenates it"""
    tag = '{{urn:oasis:names:tc:xliff:document:1.2}}{}'.format(field)
    sources = trans_unit.find(tag)
    if not sources or len(sources)<1:
       return "" 
    source_texts = trans_unit.find(tag).findall('.//{urn:oasis:names:tc:xliff:document:1.2}g')
    full_text = ""
    if len(source_texts)<1:
        return ""
    for text in source_texts:
        content = text.text
        if isinstance(content, str):
            full_text+=content
    return full_text

def add_language_from_transunit(trans_unit, dictionary={}):
    """For each trans_unit, it gets the text and appends to the dictionary of
    languages"""
    text = get_text_from_transunit(trans_unit)
    if text.isalpha():
        return dictionary_count(text, dictionary)
    else:
        return dictionary


def get_input_files(directory='raw_data'):
    """Get list of valid input files"""
    files=[]
    for filename in os.listdir(directory):
        if "sdlxliff" not in filename:
            continue
        fullpath = "{}/{}".format(directory, filename)
        if not os.path.exists(fullpath) or not os.path.isfile(fullpath):
            continue
        files.append(fullpath)
    return files

def get_text_from_file(filename, field='source'):
    """Given a file name, it gets all the (source) text from the file"""
    root = ET.parse(filename).getroot() 
    trans_units = root.findall('.//{urn:oasis:names:tc:xliff:document:1.2}trans-unit')
    text=""
    for tu in trans_units:
        if tu: 
            text+= get_text_from_transunit(tu, field)
    return text


#Example usage:
#
#for file in files: 
#    text = get_sources_from_file(file, field='source') 
#    language_dictionary= dictionary_count(text, language_dictionary) 





