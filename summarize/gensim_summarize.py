from text_parsing import get_text_from_file
from gensim.summarization.summarizer import summarize

#get sinle file
text = get_text_from_file('sample_long.sdlxliff')

try:
    # word_count : provides summary of n words
    # ratio : provides summary of percentage of text
    sum = summarize(text, word_count=100)
    #sum = summarize(text, ratio=0.1)
    print('character length is:', len(sum), '\n ######## \n', sum)
except:
    print(text)

