
import numpy as np
import pandas as pd

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

import re
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
	

	def exclude_digits(word):
		if any(char.isdigit() for char in word):
			words = re.split(r'([\d,\.,\,]+)', word)
			new_words = []
			for w in words:
				if w!='':
					if any(char.isdigit() for char in w):
						new_words.append("<num>")
					else:
						new_words.append(w)
			
			return new_words
		return [word]


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

def process_text(text):
	current_text_words = []
	word_position_list_sample = []
	past_text_len = 0

	"""
	tokens = ["<sw>",  #stopword
	"<sot>", #start of text
	"<eot>", #end of text
	"<bos>", #start of sentence
	"<eos>", #start of sentence
	"<num>", #number
	"<>"     #exclude word
	]
	"""

	current_text_words.append("<sot>")
	word_position_list_sample.append([0,0])

	for sentence in sent_tokenize(text):
        #current_text_words.append("<bos>")
		current_text_words.append("<bos>")
		word_position_list_sample.append([past_text_len,past_text_len])

		for w in word_tokenize(sentence):
            
			w_l = len(w) + 1
			left = past_text_len
			right = past_text_len + w_l
            
			past_text_len += w_l            
            
			w = WordAnalysis.preprocess_word(w)
			#collect(w)

			w = WordAnalysis.exclude_stopwords(w)
			w = WordAnalysis.exclude_punctuation_signs(w)
            
			if w == "<>":
				continue
            
			w = WordAnalysis.exclude_digits(w)
			for w1 in w:
				word_position_list_sample.append([left,right])
                #collect_after_transform(w1)
                #text_all_words_list.append(w)
				current_text_words.append(w1)
        #current_text_words.append("<eos>")

		current_text_words.append("<eos>")
		word_position_list_sample.append([past_text_len,past_text_len])
	
	current_text_words.append("<eot>")
	word_position_list_sample.append([past_text_len,past_text_len])
    
	return current_text_words, word_position_list_sample


def text_to_words_list(texts):
	text_list_of_words = []
	text_all_words_list = []
	word_position_list = []
	for text in texts:
		current_text_words, word_position_list_sample = process_text(text)
		
		text_list_of_words.append(current_text_words)
		word_position_list.append(word_position_list_sample)
		for w in current_text_words:
			text_all_words_list.append(w)
            
	return text_list_of_words, text_all_words_list, word_position_list
	