from random import randint
from enum import Enum

class Player:
    def __init__(self, name, hand=None):
        self.hand = hand

    def draw_card(self):
        pass

    
# Return a randomly sorted deck of cards
# Format: [[suit, value], [suit, value], ...]
def init_deck():
    temp_deck = [[suit, value] for suit in ["Clubs", "Hearts", "Spades", "Diamonds"] for value in range(1, 14)]

    # shuffle deck
    deck = []
    while temp_deck:
        randIdx = randint(0, len(temp_deck) - 1)
        deck.append(temp_deck[randIdx])
        del temp_deck[randIdx]
    
    return deck


class HandType(Enum):
    PAIR = 1
    FLUSH = 2
    STRAIGHT = 3
    TRIPLE = 4
    STRAIGHT_FLUSH = 5


def draw(deck, player):
    randIdx = randint(0, len(deck) - 1)
    player.append(deck[randIdx])   
    del deck[randIdx]


# Return the type of hand the player has:
# pair < flush < straight < triple < straight-flush
def get_hand_type(hand):
# OBJECT-ORIENTED PLAYERS?

    pass


def compare_hands(hand1, hand2):
    # identify type of hand1
    # identify type of hand2

    pass


def play(deck):
    human = Player("human", [])
    computer = Player("computer", [])

    # Draw first 3 cards for each player
    for i in range(3):
        draw(deck, human)
    for i in range(3):
        draw(deck, computer)

    while deck:
        # Each player draws a card
        draw(deck, human)
        draw(deck, computer)

        # compare cards


def main():
    deck = init_deck()
    play(deck)


main()