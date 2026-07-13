import random
cards = {"2": 2,
         "3": 3,
         "4": 4,
         "5": 5,
         "6": 6,
         "7": 7,
         "8": 8,
         "9": 9,
         "10": 10,
         "K": 10,
         "Q": 10,
         "J": 10,
         "A": 11}

def play_cards():
    while True:
        print("\n*************************************************************************************")
        choice_1 = input("Welcome to a game of blackjack. Would you like to play? Press y for yes and n for no: \n*************************************************************************************").lower()
        print("*************************************************************************************")
        if choice_1 == "n":
            print("Sad to see you go...")
            break
        elif choice_1 == "y":
            card_list = list(cards.keys()) * 4
            first_card = random.choice(card_list)
            card_list.remove(first_card)
            first_card_house = random.choice(card_list)
            card_list.remove(first_card_house)
            second_card = random.choice(card_list)
            card_list.remove(second_card)
            second_card_house = random.choice(card_list)
            card_list.remove(second_card_house)

            aces_as_11 = 0
            if first_card == "A": aces_as_11 += 1
            if second_card == "A": aces_as_11 += 1

            total = cards.get(first_card) + cards.get(second_card)

            if total > 21 and aces_as_11 > 0:
                total -= 10
                aces_as_11 -= 1

            house_aces_as_11 = 0
            if first_card_house == "A": house_aces_as_11 += 1
            if second_card_house == "A": house_aces_as_11 += 1

            house_total = cards.get(first_card_house) + cards.get(second_card_house)

            if house_total > 21 and house_aces_as_11 > 0:
                house_total -= 10
                house_aces_as_11 -= 1
            
            print(f"The houses first card is a {first_card_house}.")
            print(f"Your first card is a {first_card}. Your second card is a {second_card}. The total value is {total}.", end = " ")
            
            while True:
                choice_2 = input(f"Would you like to draw another card? Press y for yes and n for no: ").lower()
                if choice_2 == "n":
                    print("You stand. Let's see what the house has.")
                    break
                elif choice_2 == "y":
                    other_card = random.choice(card_list)
                    card_list.remove(other_card)

                    if other_card == "A":
                        aces_as_11 += 1

                    total += cards.get(other_card)
                    print(f"You drew a {other_card}.", end = " ")
                    
                    while total > 21 and aces_as_11 > 0:
                        total -= 10
                        aces_as_11 -= 1
                        print("Ace adjusted to 1.", end=" ")

                    if total > 21:
                        print("The total is over 21. You lost!")
                        break
                    elif total == 21:
                        print("You hit 21! Let's see what the house has.")
                        choice_2 = "n"
                        break
                    else:
                        print(f"Your new total is {total}.")

            if total <= 21:
                print(f"The houses second card is a {second_card_house}. Their total is {house_total}.")
                while house_total < 17:
                    other_card_house = random.choice(card_list)
                    card_list.remove(other_card_house)

                    if other_card_house == "A":
                        house_aces_as_11 += 1

                    house_total += cards.get(other_card_house)
                    print(f"House drew a {other_card_house}.", end = " ")
                    
                    while house_total > 21 and house_aces_as_11 > 0:
                        house_total -= 10
                        house_aces_as_11 -= 1
                        print("Ace adjusted to 1.", end=" ")

                    print(f"Houses new total is {house_total}.", end= " ")

                if house_total > 21:
                    print(f"Houses total is over 21. Your total is {total}. You won!")
                elif house_total == 21:
                    if total == 21:
                            print("Its a draw.")
                    else:
                        print("You lost.")
                elif total > house_total:
                    print("You won!")
                elif total == house_total:
                    print("It's a draw.")
                else:
                    print("You lost.")

if __name__ == "__main__":
    play_cards()