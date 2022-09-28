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


class Card:
    def __init__(self, suit, value, face_down = False):
        self.suit = suit
        self.value = value
        self.face_down = face_down


class Player:
    def __init__(self, name, hand=None):
        self.hand = hand # array of cards

    def draw_from(self, deck, face_down=False):
        randIdx = randint(0, len(deck) - 1)
        card = deck[randIdx]   
        card.face_down = face_down
        self.hand.append(card)
        del deck[randIdx]


class Game:
    def __init__(self, deck=None, bets=None):
        self.deck = deck
        self.bets = bets

    # Return a randomly sorted deck of cards
    # Format: [[suit, value], [suit, value], ...]
    def new_deck(self):
        self.deck = [Card(suit, value) for suit in [Suit.CLUBS, Suit.HEARTS, Suit.SPADES, Suit.DIAMONDS] for value in range(1, 14)]
        self.shuffle()

        # # alternative shuffle method
        # i = 0
        # while i < len(temp_deck):
        #     randIdx = randint(i, len(temp_deck) - 1)
        #     temp_deck[i], temp_deck[randIdx] = temp_deck[randIdx], temp_deck[i],
        #     i += 1

        return self.deck

    # Randomly shuffles the deck
    def shuffle(self):
        res = []
        while self.deck:
            randIdx = randint(0, len(self.deck) - 1)
            res.append(self.deck[randIdx])
            del self.deck[randIdx]
        self.deck = res

    def play(deck):
        human = Player("human", [])
        computer = Player("computer", [])

        # 1. Create a deck of cards
        # 2. User places a bet ($ amount)
        # 3. Both players are dealth three cards. 2 face up and 1 face down.
        # 4. Both players take turns to raise their bets.
        
        # User places a bet

        # Both players are dealth three cards. 2 face up and 1 face down.
        human.draw_from(deck)
        human.draw_from(deck)
        human.draw_from(deck, face_down=True)
        computer.draw_from(deck)
        computer.draw_from(deck)
        computer.draw_from(deck, face_down=True)

        # Both players take turns to raise their bets.
        while deck:
            pass

    # Return the type of hand the player has:
    def get_hand_type(hand):
        hand.sort(key = lambda card: card.value)

        value_counts = [0 for _ in range(13)]
        suit_counts = [0 for _ in range(4)]

        pair = False # two cards of same value
        flush = False # three cards of the same suit (order doesn't matter)
        straight_count = 1 # three cards in a row w/ different suits
        triple = False # three cards of same value

        prev = None
        for card in hand:
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

    # Returns
    #    1: if handOne > handTWo
    #    0: if handTwo > handOne
    #   -1: if handOne == handTow
    def compare_hands(handOne, handTwo):
        handOneType = get_hand_type(handOne)
        handTwoType = get_hand_type(handTwo)
        if handOneType > handTwoType:
            return 1
        elif handTwoType > handOneType:
            return -1
        else:
            return 0


def main():
    game = Game()
    Game.play(deck)

    # Pair: two cards of same value
    # Flush: five cards of the same suit (order doesn't matter)
    # Straight: five cards in a row w/ different suits
    # Triple: three cards of same value
    # Straight-flush: five cards in a row (all same suit)


main()