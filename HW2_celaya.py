"""
Made by: Jorge Celaya
CSCE 480
HW2


"""

import random
from random import randint
from enum import Enum

class Suit(Enum):
    CLUBS = 1
    HEARTS = 2
    SPADES = 3
    DIAMONDS = 4


class HandType(Enum):
    NONE = 0
    PAIR = 1
    FLUSH = 2
    STRAIGHT = 3
    TRIPLE = 4
    STRAIGHT_FLUSH = 5


class Plays(Enum):
    CALL = 1
    RAISE = 2
    FOLD = 3


class Card:
    def __init__(self, suit, value, face_down = False):
        self.suit = suit
        self.value = value
        self.face_down = face_down

class Player:
    def __init__(self, name, hand=None):
        self.name = name
        self.hand = hand # array of cards
        self.bet = 0.0
        self.balance = 0.0
        self.games_played = 0
        self.games_won = 0
        self.games_lost = 0
        self.win_ratio = 0
        self.game_count = 0

    def clear_hand(self):
        self.hand = []

    def draw_from(self, deck, face_down=False):
        randIdx = randint(0, len(deck) - 1)
        card = deck[randIdx]   
        card.face_down = face_down
        self.hand.append(card)
        del deck[randIdx]
    
    def place_bet(self, bet):
        self.bet = bet
        self.balance -= bet

    def calculate_choice(self, opponent):
        opponent_hand = opponent.get_hand_type()
        my_hand = self.get_hand_type()

        if self.game_count == 0:
            return random.choice(list(Plays))

        # TODO: Utilize stats to make decisions
        if my_hand.value > opponent_hand.value: # if winning hand -> raise
            if opponent.bet > self.balance:
                return random.choice([Plays.RAISE, Plays.CALL])
            else:
                return random.choice([Plays.RAISE, Plays.CALL, Plays.FOLD])
        elif my_hand.value < opponent_hand.value: # if tied -> match or 
            if opponent.bet > self.balance:
                return Plays.FOLD
            else:
                return random.choice([Plays.CALL, Plays.FOLD])
        else: # if losing hand -> fold
            if opponent.bet > self.balance:
                return Plays.FOLD
            else:
                return random.choice([Plays.CALL, Plays.FOLD])

    # Return the type of hand the player has
    def get_hand_type(self):
        self.hand.sort(key = lambda card: card.value)

        value_counts = [0 for _ in range(13)]
        suit_counts = [0 for _ in range(4)]

        pair = False # two cards of same value
        flush = False # three cards of the same suit (order doesn't matter)
        straight_count = 1 # three cards in a row w/ different suits
        triple = False # three cards of same value

        prev = None
        for card in self.hand:
            if prev and card.value == prev.value + 1:
                straight_count += 1
            
            # count cards with same value
            valueIdx = card.value - 1
            value_counts[valueIdx] += 1
            if value_counts[valueIdx] == 2:
                pair = True
            elif value_counts[valueIdx] == 3:
                triple = True
            
            # count cards with same suit
            suitIdx = card.suit.value - 1
            suit_counts[suitIdx] += 1
            if suit_counts[suitIdx] == 3:
                flush = True

            prev = card

        if straight_count == 3 and flush:
            return HandType.STRAIGHT_FLUSH
        elif triple:
            return HandType.TRIPLE
        elif straight_count == 3:
            return HandType.STRAIGHT
        elif flush:
            return HandType.FLUSH
        elif pair:
            return HandType.PAIR
        else:
            return HandType.NONE


class Game:
    def __init__(self, deck=None):
        self.deck = deck
        self.pot = 0.0
        self.user = Player("user", [])
        self.computer = Player("computer", [])
        self.current_bet = 0.0

    # Return a randomly sorted deck of cards
    # Format: [[suit, value], [suit, value], ...]
    def init_deck(self):
        self.deck = [Card(suit, value) for suit in [Suit.CLUBS, Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS] for value in range(1, 14)]
        self.shuffle_deck()

    # shuffles the deck in random fashion
    def shuffle_deck(self):
        res = []
        while self.deck:
            randIdx = randint(0, len(self.deck) - 1)
            res.append(self.deck[randIdx])
            del self.deck[randIdx]
        self.deck = res

    # Returns
    #    1: if handOne > handTWo
    #    0: if handTwo > handOne
    #   -1: if handOne == handTow
    def compare_hands(self):
        userHandType = self.user.get_hand_type()
        computerHandType = self.computer.get_hand_type()
        if userHandType.value > computerHandType.value:
            return 1
        elif computerHandType.value > userHandType.value:
            return -1
        else:
            return 0

    def show_hands_safe(self):
        print("Your hand:")
        for card in self.user.hand:
            if not card.face_down:
                print(card.suit, card.value)
        print()

        print("Computer's hand:")
        for card in self.computer.hand:
            if not card.face_down:
                print(card.suit, card.value)
        print()

    def reveal_hands(self):
        print("Your hand:")
        for card in self.user.hand:
            print(card.suit, card.value)
        print()

        print("Computer's hand:")
        for card in self.computer.hand:
            print(card.suit, card.value)
        print()

    def decide_winner(self):
        hands = ["None", "Pair", "Flush", "Straight", "Triple", "Straight-flush"]
        result = self.compare_hands()

        if result == 1:
            self.user.balance += self.pot
            print(f"You have won with a {hands[self.user.get_hand_type().value]}")
        elif result == -1:
            self.computer.balance += self.pot
            print(f"The computer has won with a {hands[self.computer.get_hand_type().value]}.")
        else:
            print(f"You have tied with the computer with a {hands[self.user.get_hand_type().value]}.")
            pot = round(self.pot / 2, 2)
            print(f"half of pot: {pot}")
            self.user.balance += pot
            self.computer.balance += pot
        
        # self.computer.update_stats(...)
        # self.user.update_stats(...)

    # Runs the game loop
        # 1. User places a bet ($ amount)
        # 2. Both players are dealt three cards. 2 face up and 1 face down.
        # 3. Both players take turns to raise their bets.
        # 4. Repeat rounds until player quits
    def play(self):
        ans = "y"

        while ans.lower() == "y" or ans.lower() == "yes":
            print()
            self.user.clear_hand()
            self.computer.clear_hand()

            # replenish deck if empty
            if len(self.deck) < 6:
                self.init_deck()
        
            # Both players are dealth three cards. 2 face up and 1 face down.
            self.user.draw_from(self.deck)
            self.user.draw_from(self.deck)
            self.user.draw_from(self.deck, face_down=True)
            self.computer.draw_from(self.deck)
            self.computer.draw_from(self.deck)
            self.computer.draw_from(self.deck, face_down=True)

            self.show_hands_safe()
            
            # User places a bet
            bet = int(input("Place your bet: "))
            self.user.place_bet(bet)
            self.current_bet = self.user.bet
            self.pot += self.user.bet

            # User: no additional bet or raise.
            # Computer: match user’s raise, match user’s raise and raise bet, or fold (give-up).
            # User (If computer did additional raise): match the raise or fold.
            computer_raised_bet = True
            user_raised_bet = True
            computer_turn = True
            folded = False
            
            # Both players take turns to raise their bets.
            while not folded and user_raised_bet and computer_raised_bet:
                print(f"pot: {self.pot}")

                if computer_turn: # Computer's turn
                    choice = self.computer.calculate_choice(self.user)
                    self.computer.game_count += 1

                    if choice == Plays.RAISE:
                        self.computer.place_bet(self.current_bet * 1.15)
                        self.current_bet = self.computer.bet
                        self.pot += self.computer.bet
                        computer_raised_bet = True
                        print(f"Computer has raised the bet to ${self.current_bet}")
                    elif choice == Plays.CALL:
                        self.computer.place_bet(self.current_bet)
                        self.pot += self.computer.bet
                        computer_raised_bet = False
                        print(f"Computer has matched the bet of ${self.current_bet}")
                    else: # fold
                        folded = True
                        self.user.balance += self.pot
                        computer_raised_bet = False
                        print(f"Computer has folded. You win ${self.pot}.")

                    computer_turn = False
                elif computer_raised_bet: # User's turn
                    print("Current hands:")
                    self.show_hands_safe()
                    print(f"Current bet: ${self.current_bet}.")
                    print("Options:\n\t1. Raise\n\t2. Match\n\t3. Fold")
                    choice = int(input("Make your Choice: "))
                    print

                    if choice == 1:
                        bet = float(input("Place your bet: "))
                        while bet <= self.current_bet:
                            print(f"Your raise should be higher than the current bet of ${self.current_bet}")
                            bet = input(f"Place your bet again: ")
                        self.user.place_bet(bet)
                        self.current_bet = bet
                        self.pot += self.user.bet
                        user_raised_bet = True
                        print(f"You have raised the bet to ${self.current_bet}.")
                    elif choice == 2:
                        self.user.place_bet(self.current_bet)
                        self.pot += self.user.bet
                        user_raised_bet = False
                        print(f"You have matched the bet of ${self.current_bet}.")
                    else: # fold
                        folded = True
                        self.computer.balance += self.pot
                        user_raised_bet = False
                        print(f"You have folded. The computer has won ${self.pot}.")
                    computer_turn = True
            
            # Reveal face down cards and decide winner
            print("\nResults:\n")
            self.reveal_hands()
            if not folded:
                self.decide_winner()

            # update stats
            # self.computer.update_stats(...)
            # self.computer.update_stats(...)
            
            print(f"\nYour current balance: {self.user.balance}, Computer's final balance: {self.computer.balance}")
            # reset pot
            self.pot = 0

            ans = input("Would you like to play another round? (y/n): ")

        print(f"\nYour final balance: {self.user.balance}, Computer's final balance: {self.computer.balance}")
        print("Thank you for playing!")


# TODO: Save/update stats in an external file to remember previous games 
def main():
    game = Game()
    game.init_deck() # Create a deck of cards
    game.play() # Run game loop


main()