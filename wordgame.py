# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 21:24:48 2022

@author: carys
"""
import numpy as np
import random
import pandas as pd
import re
from string import ascii_lowercase
import os


# -----Functions

def number_assigning(let):
    num = ascii_lowercase.find(let)
    return num+1


def compare(b, a):
    if a == b:
        answer = ('same')
    elif a > b:
        answer = ('higher')
    elif a < b:
        answer = ('lower')
    return answer


def word_generator(diction):

    dictionary = pd.read_csv(diction)

    randomnum = random.randint(1, dictionary.size)

    word = dictionary.iloc[randomnum, 0]

    return word


def guessed_word():
    guessword = []
    guess = input(('guess word '))
    guess = guess.lower()
    re.sub(r'[^a-z]*', "", guess)
    print(guess)
    for y in guess:
        guessword.append(number_assigning(y))
    return guessword


def dict_menu():
    files = os.listdir(os.getcwd()+'/dicts')
    for f in enumerate(files):
        list(f)
        print(str(f[0]+1)+'. '+f[1])
    try:
        dict_choice = int(input('Enter the number of the dictionary you want to use: '))
        choice = files[(dict_choice-1)]
    except IndexError:
        print("I'm sorry that is not a valid dictionary please try again")
        choice = dict_menu()

    return choice


def main_code():

    random_word = word_generator('dicts/' + dict_menu())

    numword = []
    for x in random_word:
        numword.append(number_assigning(x))

    guessedword = ''

    counter = 0

    while guessedword != numword:
        guessedword = guessed_word()

        if len(numword) < len(guessedword):
            for element in range(0, len(numword)):
                response = compare(guessedword[element], numword[element])
                if response == 'higher' or response == 'lower':
                    break

        else:
            for element in range(0, len(guessedword)):
                response = compare(guessedword[element], numword[element])

                if response == 'higher' or response == 'lower':
                    break

        if response == 'same':
            if len(numword) < len(guessedword):
                print('lower')
            elif len(guessedword) < len(numword):
                print('higher')
        else:
            print(response)
        counter += 1

    print('Well done, {} was the word, it took you {} guesses'.format(
        random_word, counter))
    again = input('Would you like to play again? yes or no ')
    return again

# -----Main Code


play = main_code()
while play.lower() == 'yes':
    play = main_code()
