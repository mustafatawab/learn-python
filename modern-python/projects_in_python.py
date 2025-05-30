# -*- coding: utf-8 -*-
"""Projects in Python

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12qniddnpGhz_83YiwX1GR3xJAcl73fg7

Joke Bot
"""

def print_joke() -> None:
      PROMPT : str = "what do you want?"
      user_input : str = input(PROMPT)
      if user_input.lower() == 'joke':
        print("Here is a joke for you. Every software engineer is a programmer. HAHAHA")

      else:
        print("Sorry, I just tell jokes")




print_joke()

user_input  = int(input("Enter a number"))

while user_input <= 100:
  user_input *= 2
  print(user_input , end=" ")

countDown : int  = 10
for i in range(countDown):
  countDown -= 1
  print(countDown , end=' ')
  if(countDown == 1):
    print("BOOM")

for i in range(10 , 0 , -1):
  print(i , end=' ')

print("lift off")

def countdown():
  number_list : list[int] = [10 , 9 , 8 , 7 , 6 , 5, 4, 3, 2, 1]
  for i in number_list:
    print(i , end=" ")

  print("Liftoff")

countdown()

import random

def guessGame()->str:
  number : int = random.randint(1 , 100)
  user_input = int(input("I am thinking numbers from 1 to 100. Guess the number"))
  if(user_input < number):
    return "Too Low"
  elif(user_input > number):
    return "Too High"
  elif(user_input == number):
    return "You Guess the Correct"

def TryAgain():
    print("Try Again")
    again : str = "yes"
    while True:
      print(guessGame())
      again = input("Do you want to play again? (yes or no)")
      if(again == "yes"):
        continue
      else:
        break




TryAgain()

"""Generate random numbers from 1 to 100 but total numbers should be 10"""

from random import randint

def GenerateRandomNumbers():
  MINIMUM_NUMBER : int = 1
  MAXIMUM_NUMBER : int = 100

  random_list : list[int] = []
  for i in range(1 , 10):
    randomNumber = randint(MINIMUM_NUMBER , MAXIMUM_NUMBER)
    random_list.append(randomNumber)


  # for number in random_list:
  #   print(number , end=" ")
  print(*random_list)


GenerateRandomNumbers()

import numpy as np

MINIMUM_NUMBER : int = 1
MAXIMUM_NUMBER : int = 101

random_array = np.random.randint(MINIMUM_NUMBER , MAXIMUM_NUMBER , 10)

print(*random_array)

def CalculateWeighOnMars():
  """ You have to calculate weight on mars accoring to your weight on earch  """
  MARS_CONSTANT : float = 0.378

  weight : float = float(input("Enter your weight on earth : "))

  weight_on_mars = round((weight * MARS_CONSTANT) , 2)
  print("Your weight on mars is equavalant to " , weight_on_mars)

CalculateWeighOnMars()

# prompt: write all garvity constant for all planets

# Gravity constants for all planets (in m/s^2)
PLANET_GRAVITY = {
    "Mercury": 3.7,
    "Venus": 8.87,
    "Earth": 9.807,
    "Mars": 3.711,
    "Jupiter": 24.79,
    "Saturn": 10.44,
    "Uranus": 8.69,
    "Neptune": 11.15,
    "Pluto": 0.62
}




def calculate_weight_on_planet():
    """ Calculate weight on a specific planet based on Earth weight """
    print("Available planets:")
    for planet in PLANET_GRAVITY:
        print(f"- {planet} :   {PLANET_GRAVITY[planet]}")

    planet_name = input("Enter the name of the planet in above options  ").capitalize()

    while True:
        try:
          earth_weight = float(input("Enter your weight on Earth (kg): "))
          break
        except ValueError:
          earth_weight = float(input("Please enter in number : "))
          continue

    if planet_name in PLANET_GRAVITY:
      print(f"Your weight on {planet_name} is  {(earth_weight * PLANET_GRAVITY[planet_name]):.2f}")

calculate_weight_on_planet()



