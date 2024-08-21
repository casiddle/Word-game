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
    """
    This function takes a letter and assigns it a numerical value based on where it is in the
    alphabet, i.e. a=1 b=2 ...

    Parameters
    ----------
    let : string with length 1 i.e. a single character

    Returns
    -------
    The assigned number value of the letter


    """
    num = ascii_lowercase.find(let)
    return num+1


def compare(b, a):
    """
    Function compares two numerical values b and a, and returns whether they are the same,
    if a is higher or if a is lower than b

    Parameters
    ----------
    b : integer
    a : integer

    Returns
    -------
    answer : string

    """
    if a == b:
        answer = ('same')
    elif a > b:
        answer = ('higher')
    elif a < b:
        answer = ('lower')
    return answer


def word_generator(diction):
    """
    function takes the dictionary the user wants to use and picks a random word from that dictionary


    Parameters
    ----------
    diction : string

    Returns
    -------
    word : string

    """

    dictionary = pd.read_csv(diction)

    randomnum = random.randint(1, dictionary.size)

    word = dictionary.iloc[randomnum, 0]

    return word


def guessed_word():
    """
    Function asks the user to guess a word or to give up, if they give up they function returns 1, if
    they guess a word it returns the numerical equivalent as a list e.g. cat -> [3,1,20]

    Returns
    -------
    guessword: list of integers

    """
    guessword = []
    guess = input(('guess word or press 1 to give up: '))
    if (guess) == '1':
        return '1'

    else:
        guess = guess.lower()
        re.sub(r'[^a-z]*', "", guess)
        print(guess)
        for y in guess:
            guessword.append(number_assigning(y))
            # print(guessword)
        return guessword


def dict_menu():
    """
    Creates a menu of possible dictionaries for the word to be chosen from and returns the choice

    Returns
    -------
    choice : string
    """
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


def word_analysis(word, count):
    """
    Takes and stores the word and the number of guesses for the user to get the word

    Parameters
    ----------
    word : string
    count : integer

    Returns
    -------
    None.

    """
    with open('word_analysis.csv', 'a') as file:
        file.write(word+','+str(count)+'\n')
    return None


def main_code():

    random_word = word_generator('dicts/' + dict_menu())

    numword = []
    for x in random_word:
        numword.append(number_assigning(x))

    guessedword = ''

    counter = 0

    while guessedword != numword:
        guessedword = guessed_word()
        if guessedword == '1':
            print('Quitter! Your word was {}'.format(random_word))
            guessedword = numword

        else:

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
            if guessedword == numword:
                print('Well done, {} was the word, it took you {} guesses'.format(
                    random_word, counter))
                word_analysis(random_word, counter)

    again = input('Would you like to play again? yes or no ')
    return again

# -----Main Code


play = main_code()
while play.lower() == 'yes':
    play = main_code()
