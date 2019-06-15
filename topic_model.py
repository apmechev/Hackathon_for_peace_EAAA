import gensim 
from gensim import corpora
from gensim.corpora import Dictionary
import pickle
import os
from spacy.lang.en import English 
import nltk

from nltk.corpus import wordnet as wn 
def get_lemma(word): 
    lemma = wn.morphy(word) 
    if lemma is None: 
        return word 
    else: 
        return lemma 
     
from nltk.stem.wordnet import WordNetLemmatizer 
def get_lemma2(word): 
    return WordNetLemmatizer().lemmatize(word) 


en_stop = set(nltk.corpus.stopwords.words('english'))
parser = English() 

eng_only_files = pickle.load(open('english_only_files.pkl','rb'))
eng_only_files=[i.strip('.doc.sdlxliff').replace('raw_data/','data_products/extracted/')+".txt" for i in eng_only_files]




NUM_TOPICS = 20

def tokenize(text): 
    lda_tokens = [] 
    tokens = parser(text) 
    for token in tokens: 
        if token.orth_.isspace(): 
            continue 
        elif token.like_url: 
            lda_tokens.append('URL') 
        elif token.orth_.startswith('@'): 
            lda_tokens.append('SCREEN_NAME') 
        else: 
            lda_tokens.append(token.lower_) 
    return lda_tokens 



def load_data(files_list):
    text_data=[]
    for filename in files_list:
        text_data.append(prepare_text_for_lda(open(filename,'r').read()))
    return text_data


def get_dict_and_corpus(text_data):
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    return dictionary,corpus



def prepare_text_for_lda(text): 
    tokens = tokenize(text) 
    tokens = [token for token in tokens if len(token) > 4] 
    tokens = [token for token in tokens if token not in en_stop] 
    tokens = [get_lemma(token) for token in tokens] 
    return tokens 


def predict_topics_from_file(filename, dictionary_file='dictionary.gensim',
        model='models/model30.gensim'):
    new_doc = open(filename,'r').read()
    predict_topic_from_text(new_doc, dictionary_file=dictionary_file,
            model=model)

def predict_topic_from_text(new_doc,  dictionary_file='dictionary.gensim',
        model='models/model30.gensim', printout=False):
    ldamodel = gensim.models.ldamodel.LdaModel.load(model)  
    new_doc = prepare_text_for_lda(new_doc)
    dictionary=Dictionary.load( dictionary_file)
    new_doc_bow = dictionary.doc2bow(new_doc)
    doc_topics = sorted(ldamodel.get_document_topics(new_doc_bow),key=lambda x:x[1], reverse=True)
    all_topics = ldamodel.show_topics(30)
    thresh_topics=[]
    for topic in doc_topics:
        if topic[1]>0.1:
            thresh_topics.append({'topic #':all_topics[topic[0]][0],"topic probability":
                topic[1],'topic hot words': all_topics[topic[0]][1]})
    if printout:
        print(thresh_topics)
    return thresh_topics
    


