from flask import Flask, render_template, request, jsonify, session
import numpy as np
import random
import pandas as pd
import re
from string import ascii_lowercase
import os
import secrets


app= Flask(__name__)
app.secret_key=secrets.token_hex(16)

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


def guessed_word(guess):
    guessword = []
    #guess = input(('guess word '))
    #guess = guess.lower()
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



@app.route("/")
def index():
  return render_template("index.html")

@app.route('/start_game', methods=['POST'])
def start_game():
    try:
        random_word = word_generator(r"dicts\easy.txt.csv")
        numword = [number_assigning(char) for char in random_word]

        session['numword'] = numword
        session['random_word'] = random_word
        session['counter'] = 0
        session["guess_history"]=[]

        return jsonify({"word_length": len(random_word), "word":random_word})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500

@app.route('/guess', methods=['POST'])
def guess():
    try:
        # Retrieve guess and session variables
        guessed_word = request.json.get('guess', '').lower()
        numword = session.get('numword')
        random_word = session.get('random_word')
        counter = session.get('counter', 0)
        history=session.get("guess_history",[])

        if numword is None or random_word is None:
            return jsonify({"error": "Game has not started or session expired"}), 400

        guessed_word_numbers = [number_assigning(char) for char in guessed_word]

        # Initialize response and message
        response = 'wrong'
        message = 'Incorrect guess, try again!'

        # Compare guessed word with the target word
        if guessed_word_numbers == numword:
            response = 'correct'
            message = f"Well done, {random_word} was the word, it took you {counter + 1} guesses."
        else:
            # Provide feedback based on the comparison
            for i in range(min(len(numword), len(guessed_word_numbers))):
                comp_result = compare(guessed_word_numbers[i], numword[i])
                if comp_result in ['higher', 'lower']:
                    message = f"Guess is too {comp_result}."
                    response=f"{comp_result}"
                    break
        #Update guess history
        guess_result={
            "guess":guessed_word, 
            "result":response,
            "message":message
        }
      
        history.append(guess_result)
        session["guess_history"]=history
        # Update the guess counter in the session
        session['counter'] = counter + 1

        return jsonify({"result": response, "message": message, "history":history})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)

