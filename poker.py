from random import randint
from enum import Enum

class Suit(Enum):
    CLUBS = 1,
    HEARTS = 2,
    SPADES = 3,
    DIAMONDS = 4


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value


class Player:
    def __init__(self, name, hand=None):
        self.hand = hand # array of cards

    def draw(self, deck):
        randIdx = randint(0, len(deck) - 1)
        self.append(deck[randIdx])   
        del deck[randIdx]

        
class HandType(Enum):
    PAIR = 1
    FLUSH = 2
    STRAIGHT = 3
    TRIPLE = 4
    STRAIGHT_FLUSH = 5


# Return a randomly sorted deck of cards
# Format: [[suit, value], [suit, value], ...]
def init_deck():
    temp_deck = [Card(suit, value) for suit in ["Clubs", "Hearts", "Spades", "Diamonds"] for value in range(1, 14)]

    # shuffle deck
    deck = []
    while temp_deck:
        randIdx = randint(0, len(temp_deck) - 1)
        deck.append(temp_deck[randIdx])
        del temp_deck[randIdx]
    
    # # alternative shuffle method
    # i = 0
    # while i < len(temp_deck):
    #     randIdx = randint(i, len(temp_deck) - 1)
    #     temp_deck[i], temp_deck[randIdx] = temp_deck[randIdx], temp_deck[i],
    #     i += 1

    return deck


# Return the type of hand the player has:
def get_hand_type(hand):
    hand.sort(key = lambda card: card.value)

    value_counts = [0 for _ in range(13)]
    suit_counts = [0 for _ in range(4)]

    pair = False # two cards of same value
    flush = False # three cards of the same suit (order doesn't matter)
    straight = False # three cards in a row w/ different suits
    straigh_flush = False # three cards in a row (all same suit)

    for card in hand:
        # check for cards in a row
        hand.sort(key = lambda card: card.value)
        count = 0
        for i in range(1, len(hand)):
            if hand[i].value == hand[i - 1].value - 1:
                count += 1
        if count == 3:
            in_a_row = True
        
        # count cards with same value
        valueIdx = card.value - 1
        value_counts[valueIdx] += 1
        if value_counts[valueIdx] == 2:
            return HandType.PAIR
        
        # count cards with same suit
        suitIdx = card.suit.value - 1
        suit_counts[suitIdx] += 1
        if suit_counts[suit_counts] == 3:
            return HandType.FLUSH


    # count cards with same value and suit
    pass


# Return the better hand 
# Ordering: Pair < Flush < Straight < Triple < Straight-flush
def compare_hands(hand1, hand2):
    # identify type of hand1
    # identify type of hand2

    pass


def play(deck):
    human = Player("human", [])
    computer = Player("computer", [])

    # Draw first 3 cards for each player
    for i in range(3):
        human.draw(deck)
    for i in range(3):
        computer.draw(deck)

    print(human.hand)
    print(computer.hand)

    # while deck:
    #     # Each player draws a card
    #     human.draw(deck)
    #     computer.draw(deck)

    #     print(human.hand)
    #     print(computer.hand)
    #     # compare cards


def main():
    deck = init_deck()
    # for card in deck:
    #     print(card.suit, card.value)
    play(deck)


main()