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
    print("comparison: "+answer)
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





@app.route("/")
def index():
  return render_template("index.html")

@app.route('/start_game', methods=['POST'])
def start_game():
    try:
      data = request.get_json()
      dictionary_choice = data.get('dictionary_choice')
    
      if not dictionary_choice:
        return jsonify({"error": "Dictionary choice is required"}), 400
     # dictionary_choice = request.form['dictionary_choice']
      random_word = word_generator('dicts/' + dictionary_choice)
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
    data = request.get_json()
    print(f"Received data: {data}")  # Debug line
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
        response = 'default'
        message = 'default'

        # Compare guessed word with the target word
        if guessed_word_numbers == numword:
            response = 'correct'
            message = f"Well done, {random_word} was the word, it took you {counter + 1} guesses."
        else:
            # Provide feedback based on the comparison
            #for i in range(min(len(numword), len(guessed_word_numbers))):
            for i in range(len(numword)):
                comp_result = compare(guessed_word_numbers[i], numword[i])
                if comp_result in ['higher', 'lower']:
                    message = f"Guess is wrong."
                    response=f"{comp_result}"
                elif comp_result=="same":
                    if len(guessed_word_numbers)>len(numword):
                        message = f"Guess is too high."
                        response=f"lower"
                        comp_result="lower"
                    else:
                        message = f"Guess is too low."
                        response=f"higher"
                        comp_result="lower"


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
    
@app.route('/give_up', methods=['GET'])
def give_up():
    try:
        # Retrieve the current word from the session or where it's stored
        word = session.get('random_word') 
        counter=session.get("counter")

        if not word:
            return jsonify({"error": "No game in progress"}), 400

        return jsonify({"word": word, "counter":counter})

    except Exception as e:
        print(f"Error in /give_up: {e}")  # Log the error
        return jsonify({"error": "An error occurred while processing the give up request"}), 500


if __name__ == "__main__":
    app.run(debug=True)

