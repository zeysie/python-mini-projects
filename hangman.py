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

words = ["apple", "pear", "orange", "pinapple", "tomato"]

def hangman_game():
    print("-" * 31)
    print("Welcome to the game of Hangman.")
    print("-" * 31)

    word = random.choice(words)
    print("_" * len(word))

    counter = 0
    new_print = "_" * len(word)
    hangman_pic = ""
    guessed_letters = []
    while True:
        if counter == 7:
            print(f"\nYou lose! The word was {word}.", end= " ")
            if ask_play_again():
                words.remove(word)
                if len(words) == 0:
                        print("\nYou guessed all the words in the game. Thanks for playing!")
                        break
                word = random.choice(words)
                counter = 0
                new_print = "_" * len(word)
                hangman_pic = ""
                guessed_letters = []
                print(new_print)
                continue
            else:
                break
        letter = input("\nEnter the letter you would like to check: ").lower()
        if not letter.isalpha():
            print("\nInvalid input. Please enter a letter.")
            continue
        if letter in guessed_letters:
            print("\nYou already guessed that letter.")
            continue
        if len(letter) > 1:
            if letter == word:
                print("\nYou guessed correctly!", end=" ")
                if ask_play_again():
                    words.remove(word)
                    if len(words) == 0:
                        print("\nYou guessed all the words in the game. Thanks for playing!")
                        break
                    word = random.choice(words)
                    counter = 0
                    new_print = "_" * len(word)
                    hangman_pic = ""
                    guessed_letters = []
                    print(new_print)
                    continue
            else:
                print("\nInvalid input. Please enter a single letter.")
                continue
        if letter in word:
            newest_print = hangman_print(word, letter, new_print)
            print(hangman_pic)
            print(newest_print)
            if newest_print == word:
                print("\nYou won!", end= " ")
                if ask_play_again():
                    words.remove(word)
                    if len(words) == 0:
                        print("\nYou guessed all the words in the game. Thanks for playing!")
                        break
                    word = random.choice(words)
                    counter = 0
                    new_print = "_" * len(word)
                    hangman_pic = ""
                    guessed_letters = []
                    print(new_print)
                    continue
                else:
                    break
            new_print = newest_print
        else:
            print("\nThe letter is not in the word.")
            hangman_pic = hangman_parts[counter]
            print(hangman_pic)
            counter += 1
            print(new_print)
        guessed_letters.append(letter)

def hangman_print(word, letter, new_print):
    indexes = []
    counter = 0
    for let in word:
        if letter == let:
            indexes.append(counter)
            counter += 1
        else: counter += 1
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

if __name__ == "__main__":
    hangman_game()