
import numpy as np
import pandas as pd

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')

class WordAnalysis():
	tokens = ["<sw>",  #stopword
	          "<sot>", #start of text
	          "<eot>", #end of text
	          "<bos>", #start of sentence
	          "<eos>", #start of sentence
	          "<num>", #number
	          "<>"     #exclude word
	          ]

	def preprocess_word(word):
	    word = word.lower()
	    return word
	    
	def exclude_stopwords(word):
		
		stop_words = set(stopwords.words('russian'))
		if word in stop_words:
			return "<sw>"
		return word


	def exclude_punctuation_signs(word):
	    if word in "().,?/!@№":
	        return "<>"
	    return word
	    pass

	def exclude_digits(word):
	    if any(char.isdigit() for char in word):
	        return "<num>"
	    return word


def extracted_p_process(df_extracted_part,column):
    res = []
    for items in list(df_extracted_part[column]):
        if len(items)==1:
            res.append(items[0])
        else:
            raise Error("Only one fragment expected")
    return pd.Series(res)



def process_train_df(df_train):
	#df_train = pd.read_json(file_path)

	df_extracted_part = pd.DataFrame.from_records(list(df_train['extracted_part']))
	for c in df_extracted_part.columns:
	    df_extracted_part[c] = extracted_p_process(df_extracted_part,c)

	#df_extracted_part.head(3)

	df = pd.concat([df_train,df_extracted_part],axis=1)
	df = df.drop(['extracted_part'],axis=1)

	df.columns = pd.Index(['id', 'text', 'label', 'text_output', 'answer_start', 'answer_end'])

	return df
	
	#df.head(5)

def df_to_words_list(df):
	wordAnalysis = WordAnalysis()
	text_list_of_words = []
	text_all_words_list = []

	for text in df.text:
	    current_text_words = []
	    for sentence in sent_tokenize(text):
	        for w in word_tokenize(sentence):
	            
	            w = WordAnalysis.preprocess_word(w)
	            w = WordAnalysis.exclude_stopwords(w)
	            w = WordAnalysis.exclude_punctuation_signs(w)
	            w = WordAnalysis.exclude_digits(w)
	            if w == "<>":
	                continue
	            text_all_words_list.append(w)
	            current_text_words.append(w)
	    text_list_of_words.append(current_text_words)

	return text_list_of_words,text_all_words_list