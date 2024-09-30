# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:02:34 2023

@author: carys
"""

#import nltk
import csv
# nltk.download('popular')
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer


def dict_gen(file_name):
    file = open(file_name, 'r',encoding='utf-8')
    words = file.read()
    words = words.lower()

    #tokenizer = RegexpTokenizer(r'[a-z]\w+\w{3}')
    #tokenizer = RegexpTokenizer(r'\b[a-z]+[a-z]{3}')
    tokenizer = RegexpTokenizer(r'\b[a-z]+[a-z]')
    string = tokenizer.tokenize(words)
    no_duplicates = list(set(string))
    #print(no_duplicates)
    with open('dicts/'+("dictionary_complete"+'.csv'), 'w') as new_dict:
        new_dict.write('\n'.join(no_duplicates))


dict_gen('text_files/Oxford English Dictionary.txt')
