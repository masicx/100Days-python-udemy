import random
import os
from game_data import data
import sys

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the parent directory
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to sys.path
sys.path.append(parent_dir)

import art

is_game_over = False
score = 0
compare_a = random.choice(data)

while not is_game_over:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(art.HIGHER_LOWER)

    if score > 0:
        print(f"You're right! Current score: {score}.")
    compare_b = random.choice(data)
    while compare_a == compare_b:
        compare_b = random.choice(data)
    
    print(f"Comparer A: {compare_a['name']}, a {compare_a['description']}, from {compare_a['country']}.")
    print(art.HIGHER_LOWER_VS)
    print(f"Against B: {compare_b['name']}, a {compare_b['description']}, from {compare_b['country']}.")
    guess = input("Who has more followers? Type 'A' or 'B': ").upper()

    if (guess == 'A' and compare_a['follower_count'] > compare_b['follower_count']) or (guess == 'B' and compare_b['follower_count'] > compare_a['follower_count']):
        score += 1
        compare_a = compare_b
    else:
        is_game_over = True

os.system('cls' if os.name == 'nt' else 'clear')
print(art.HIGHER_LOWER)   
print(f"Sorry, that's wrong. Final score: {score}.")
        