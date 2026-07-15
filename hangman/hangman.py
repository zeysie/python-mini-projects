import random

hangman_parts = [
r"""
    
  O 
    
     
   """,
r"""
    
  O 
  | 
   """,
r"""
    
  O 
  | 
 /  """,
r"""
    
  O 
  | 
 / \ """,
r"""
    
  O 
 /| 
 / \ """,
r"""
  O 
 /|\ 
 / \ """,
r"""
  | 
  O 
 /|\ 
 / \ """
]

words = []

with open("words.txt", "r") as file:
    for line in file:
        clean_word = line.strip().lower() 
        words.append(clean_word)

def hangman_game():
    print("-" * 31)
    print("Welcome to the game of Hangman.")
    print("-" * 31)

    word = random.choice(words)
    print(" ".join("_" * len(word)))

    counter = 0
    new_print = "_" * len(word)
    hangman_pic = ""
    guesses = []
    while True:
        if counter == 7:
            print(f"\nYou lose! The word was {word}.", end= " ")
            if ask_play_again():
                words.remove(word)
                word, counter, new_print, hangman_pic, guesses = reset_game()
                continue
            else:
                break
        letter = input("\nEnter the letter you would like to check: ").lower()
        if not letter.isalpha():
            print("\nInvalid input. Please enter a letter.")
            continue
        if letter in guesses:
            print("\nYou already guessed that.")
            continue
        if len(letter) > 1:
            if letter == word:
                print("\nYou guessed correctly!", end=" ")
                if ask_play_again():
                    words.remove(word)
                    word, counter, new_print, hangman_pic, guesses = reset_game()
                    continue
            else:
                print(f"\n{letter} is not the word.")
                hangman_pic = hangman_parts[counter]
                print(hangman_pic)
                print()
                counter += 1
                print(" ".join(new_print))
                guesses.append(letter)
                continue
        if letter in word:
            newest_print = hangman_print(word, letter, new_print)
            print(hangman_pic)
            print()
            print(" ".join(newest_print))
            if newest_print == word:
                print("\nYou won!", end= " ")
                if ask_play_again():
                    words.remove(word)
                    word, counter, new_print, hangman_pic, guesses = reset_game()
                    continue
                else:
                    break
            new_print = newest_print
        else:
            print("\nThe letter is not in the word.")
            hangman_pic = hangman_parts[counter]
            print(hangman_pic)
            print()
            counter += 1
            print(" ".join(new_print))
        guesses.append(letter)

def hangman_print(word, letter, new_print):
    indexes = []
    counter = 0
    for let in word:
        if letter == let:
            indexes.append(counter)
        counter += 1
    newest_print = ""
    for i in range(len(new_print)):
        if i in indexes:
            newest_print += letter
        elif new_print[i] == "_":
            newest_print += "_"
        else:
            newest_print += new_print[i]
    return newest_print

def ask_play_again():
    again_choice = ""
    while again_choice not in ["y", "n"]:
        if again_choice == "":
            again_choice = input("Would you like to try again? (y/n): ").lower()
        else:
            print("\nInvalid input.", end= " ")
            again_choice = input("Please press y for yes and n for no: ").lower()
    
    if again_choice == "n":
        print("\nThanks for playing!")
        return False
    elif again_choice == "y":
        return True

def reset_game():
    word = random.choice(words)
    counter = 0
    new_print = "_" * len(word)
    hangman_pic = ""
    guesses = []
    print(" ".join(new_print))
    return word, counter, new_print, hangman_pic, guesses

if __name__ == "__main__":
    hangman_game()