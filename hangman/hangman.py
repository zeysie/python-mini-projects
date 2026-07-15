import random

hangman_parts = [
r"""
 ________
|    
|    
|    
|     
|   """,
r"""
 ________
|    
|   O 
|    
|     
|   """,
r"""
 ________
|    
|   O 
|   |
|     
|   """,
r"""
 ________
|    
|   O 
|   | 
|  /  
|   """,
r"""
 ________
|    
|   O 
|   | 
|  / \   
|   """,
r"""
 ________
|    
|   O 
|  /| 
|  / \   
|   """,
r"""
 ________
|    
|   O 
|  /|\
|  / \   
|   """,
r"""
 ________
|   |
|   O 
|  /|\
|  / \   
|   """,
]

words = []

with open("words.txt", "r") as file:
    for line in file:
        clean_word = line.strip().lower() 
        words.append(clean_word)


def main():
    print("-" * 31)
    print("Welcome to the game of Hangman.")
    print("-" * 31)

    is_playing = True
    
    while is_playing:
        play_round()
        while True:
            again_choice = input("Would you like to try again? (y/n): ").lower()
            if again_choice not in ["y", "n"]:
                print("\nInvalid input. Please press y for yes and n for no.")
                continue
            elif again_choice == "n":
                print("\nThanks for playing!")
                is_playing = False
                break
            elif again_choice == "y":
                break


def play_round():
    word = random.choice(words)

    wrong_guess_counter = 0
    guesses = []

    print_hangman(wrong_guess_counter, "_" * len(word))

    while True:
        if wrong_guess_counter == 7:
            print(f"\nYou lost. The word was {word}.", end=" ")
            return
        guess = input("\nEnter the letter or word you would like to check: ").lower()

        # Check validity
        if not guess.isalpha():
            print("\nInvalid input. Please enter a letter or a word.")
            continue
        elif guess in guesses:
            print("\nYou already guessed that.")
            continue
        
        guesses.append(guess)

        new_print = current_print(guesses, word)

        if new_print == word:
            print()
            print(" ".join(new_print))
            print(f"\nYou guessed correctly!", end=" ")
            return

        # Check and respond according to the guesses lenght
        if len(guess) > 1:
            if guess == word:
                print()
                print(" ".join(word))
                print("\nYou guessed correctly!", end=" ")
                return
            else:
                wrong_guess_counter += 1
                print(f"\n{guess} is not the word.")
                print_hangman(wrong_guess_counter, new_print)
                continue
        else:
            if guess in word:
                print_hangman(wrong_guess_counter, new_print)
                continue
            else:
                wrong_guess_counter += 1
                print("\nThe letter is not in the word.")
                print_hangman(wrong_guess_counter, new_print)
                continue


def current_print(guesses, word):
    new_print = ""
    for letter in word:
        if letter in guesses:
            new_print += letter
        else:
            new_print += "_"
    return new_print

def print_hangman(wrong_guess_counter, new_print):
    print(hangman_parts[wrong_guess_counter])
    print(" ".join(new_print))

if __name__ == "__main__":
    main()