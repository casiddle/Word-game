# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 21:24:48 2022

@author: carys
"""
import numpy as np
import random
import pandas as pd
import re


# -----Functions

def number_assigning(let):
    if let == 'a':
        num = 1
    elif let == 'b':
        num = 2
    elif let == 'c':
        num = 3
    elif let == 'd':
        num = 4
    elif let == 'e':
        num = 5
    elif let == 'f':
        num = 6
    elif let == 'g':
        num = 7
    elif let == 'h':
        num = 8
    elif let == 'i':
        num = 9
    elif let == 'j':
        num = 10
    elif let == 'k':
        num = 11
    elif let == 'l':
        num = 12
    elif let == 'm':
        num = 13
    elif let == 'n':
        num = 14
    elif let == 'o':
        num = 15
    elif let == 'p':
        num = 16
    elif let == 'q':
        num = 17
    elif let == 'r':
        num = 18
    elif let == 's':
        num = 19
    elif let == 't':
        num = 20
    elif let == 'u':
        num = 21
    elif let == 'v':
        num = 22
    elif let == 'w':
        num = 23
    elif let == 'x':
        num = 24
    elif let == 'y':
        num = 25
    elif let == 'z':
        num = 26
    return(num)


def compare(b, a):
    if a == b:
        answer = ('same')
    elif a > b:
        answer = ('higher')
    elif a < b:
        answer = ('lower')
    return answer


def word_generator():

    #words = np.genfromtxt('dictionary.csv', dtype='float', delimiter=',', skip_header=0)
    randomnum = random.randint(1, 32304)
    df = pd.read_csv('dictionary.csv')
    word = df.iloc[randomnum, 0]
    return word


def guessed_word():
    guessword = []
    # try:
    guess = input(('guess word '))
    guess = guess.lower()
    re.sub(r'[^a-z]*', "", guess)
    print(guess)
    # except
    for y in guess:
        guessword.append(number_assigning(y))
    return guessword


def main_code():
    random_word = word_generator()

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
    again = input('Would you like to play again? ')
    return again

# -----Main Code


main_code()
while main_code() in ('yes', 'YES', 'Yes'):
    main_code()
