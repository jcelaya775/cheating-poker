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
        self.name = name
        self.hand = hand # array of cards

    def draw_from(self, deck, face_down=False):
        randIdx = randint(0, len(deck) - 1)
        card = deck[randIdx]   
        card.face_down = face_down
        self.hand.append(card)
        del deck[randIdx]
    
    def place_bet(self, bet):
        self.bet = bet

    def make_choice(self, option):
        # TODO: update current bet in Game class
            # Use stats to make smarted decisions
        if option == 1:
            pass
        elif option == 2:
            self.place_bet()
            pass
        else:
            # fold
            pass

    def calculate_choice(self, opponent):
        opponent_hand = opponent.get_hand_type()
        my_hand = self.get_hand_type()

        if my_hand.value > opponent_hand.value:
            # if winning hand -> raise
            return 2
        elif my_hand.value < opponent_hand.value:
            # if tied -> match
            return 1
        else:
            # if losing hand -> fold
            return 3

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
        self.bet = 0

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
        pass
    
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
        result = self.compare_hands()
        if result == 1:
            print(f"You have won with a {self.user.get_hand_type()}!")
        elif result == -1:
            print(f"The computer has won with a {self.computer.get_hand_type()}.")
        else:
            print(f"You have tied with the computer with a {self.user.get_hand_type()}.")

    # Runs the game loop
    def play(self):
        self.user = Player("user", [])
        self.computer = Player("computer", [])

        # 1. Create a deck of cards
        # 2. User places a bet ($ amount)
        # 3. Both players are dealt three cards. 2 face up and 1 face down.
        # 4. Both players take turns to raise their bets.

        # User places a bet
        self.bet = int(input("Place your bet: "))
        self.user.place_bet()

        # Both players are dealth three cards. 2 face up and 1 face down.
        self.user.draw_from(self.deck)
        self.user.draw_from(self.deck)
        self.user.draw_from(self.deck, face_down=True)
        self.computer.draw_from(self.deck)
        self.computer.draw_from(self.deck)
        self.computer.draw_from(self.deck, face_down=True)

        # User: no additional bet or raise.
        # Computer: match user’s raise, match user’s raise and raise bet, or fold (give-up).
        # User (If computer did additional raise): match the raise or fold.
        user_placed_bet = True
        computer_placed_bet = False
        
        # Both players take turns to raise their bets.
        while user_placed_bet and computer_placed_bet:
            if user_placed_bet: # Computer's turn
                option = self.computer.calculate_choice(self.user)

                if option == 2:
                    computer_placed_bet = True
                else:
                    computer_placed_bet = False

                self.computer.make_choice(option)
            else: # User's turn
                # TODO: make a function that handles displaying information to the console.
                option = input("""Current bet: ${computer.bet}. Choose your option:
                                        1. Match
                                        2. Raise
                                        3. Fold""")

                if option == 2:
                    user_placed_bet = True
                else:
                    user_placed_bet = False
                    
                self.user.make_choice(option)
        
        # Reveal face down cards and decide winner
        self.reveal_hands()
        self.decide_winner()


def main():
    game = Game()
    game.init_deck()
    Game.play()


main()