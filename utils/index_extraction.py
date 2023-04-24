import numpy as np

#import pandas_profiling

import re

import matplotlib.pyplot as plt



def search_fragment_index(text,left,right):
    res = []

    for i,[l,r] in enumerate(text):

        if (l> left) and len(res)==0:
            #print("start",i,l,r)
            res.append(i)

        if (l> left) and (l > right):
            #print("end",i,l,r)
            res.append(i)
            break
    return res


def get_seq_start(seq,true_seq):
    #seq = text_list_of_words[0][res[0]-5:res[1]+20]
    #true_seq = output_text_list_of_words[0]
    res = []
    res_conf = []
    
    for i,w in enumerate(seq):
        if w == true_seq[2]:
            start = i
            
            conf,end_pos = get_seq_end(i,seq[i:],true_seq[2:])
            if conf>0.5:
                res.append([start,start+end_pos])
                res_conf.append(conf)
    
    if len(res_conf)==0:
        return [res,res_conf],res
    return [res,res_conf],res[np.argmax(res_conf)]
    
                
        
def get_seq_end(start,seq,true_seq):
    #seq = text_list_of_words[0][r1[0]+res[0]-5:right]
    #true_seq = output_text_list_of_words[0]
    l = len(true_seq)
    right = l

    val = 0
    for i,(w1,w2) in enumerate(zip(seq[:right],
                             true_seq)):
        if w1==w2:
            val += 1
    
    return val/l,right

    

#print(r1[0]+res[0]-5,right,val/l)

def get_correct_fragment_positon(lengh_list,text,text_fragment,true_start,true_end):
    #lengh_list = word_position_list[0]
    #text = word_position_list[0]
    #text_fragment = output_text_list_of_words[0]
    #true_start = df['answer_start'][0]
    #true_end = df['answer_end'][0]
    
    res = search_fragment_index(lengh_list,true_start,true_end)
    start,end = res[0],res[1]
    res1,res_out = get_seq_start(text[start-5:end+20],text_fragment)
    
    if len(res1[0])==0:
    #if len(res1[0])>1 or len(res1[0])==0:
        print("res",res1);print("full text",text);print("text",text[start-5:end+20]);print("output",text_fragment)
        
    start,end = res_out[0]+res[0]-5,res_out[1]+res[0]-5
    
    return start,end

def extract_word_position_from_texts(word_position_list,text_list_of_words,output_text_list_of_words,df):    
    counter = 0
    words_index = []
    for pos,text,text_fragment,s,e in zip(word_position_list,text_list_of_words,output_text_list_of_words,list(df.answer_start),list(df.answer_end)):
        if s==0:
            words_index.append([0,0])
            continue
        start,end = get_correct_fragment_positon(pos,text,text_fragment,s,e)
        words_index.append([start,end])

        counter += 1
    return words_index