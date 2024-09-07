# Carys' Word Game
## Introduction
This game started as a way to pass time, perhaps while waiting for the level crossing to go up or on long car journeys. Initially it was played with numbers. Person A would think of a number between 1 and 1,000,000 and the others would try and guess it by saying numbers to which person A would respond higher or lower until the number was guessed. Unfortuanately, I then learned about sorting algorithms, specifically the binary search, which rather took the fun out of the game. The problem was, in theory, we knew all the numbers so could easily split the list of possible numbers in half until the correct one was found. To overcome this issue the game was modified, instead of guessing a number you had to guess a word.  
  
The switch to words was effective as nobody (except perhaps the most advanced lexicographers) knows every single word. It was quite simple to convert the higher or lower system, simply determining that whether a word was "higher" or "lower" would depend on a words position in the dictionary (in practice a numberical value was assigne to each character). For example "apple" would be lower than "cat" and "cat" lower than "caterpillar". I have had some push back on this, with some people suggesting that words beginning with "a" should be higher and "z" should be lower, I respectfully disagrre and will not be chnaging the system.

## The basic Game

## Webpage
In order to play the game through a webpage you only need the following files  
1. dicts  
2. static  
3. templates  
4. main_app.py