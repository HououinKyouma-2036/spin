import random
import time
import os
import sys

def clear_screen():
    os.system('cls' if sys.platform == 'win32' else 'clear')

def spinning_animation(names, rounds=3):
    for _ in range(rounds * len(names)):
        clear_screen()
        print("\nSpinning the wheel...\n")
        print("      ↓")
        for name in names:
            print(f"   {name}")
        time.sleep(0.2)
        # Rotate the list
        names = names[1:] + names[:1]
    return names


names = []
for i in range(4):
    name = input(f"Enter name {i+1}: ")
    names.append(name)


places = ["FIRST", "SECOND", "THIRD", "LAST"]
place_index = 0

while len(names) > 0:
    print("\nPress Enter to spin the wheel!")
    input()
    
    names = spinning_animation(names)
    
    winner = random.choice(names)
    
    print(f"\n🎉 {winner} comes in {places[place_index]} place! 🎉")
    
    names.remove(winner)
    place_index += 1
    
    if names:
        print(f"\nRemaining contestants: {', '.join(names)}")
        time.sleep(2)

print("\nGame Over! Thanks for playing!")