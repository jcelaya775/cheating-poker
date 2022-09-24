from random import randint

# Create a deck of cards format: [[suit, value], [suit, value], ...]
temp = [[suit, value] for suit in ["Clubs", "Hearts", "Spades", "Diamonds"] for value in range(1, 14)]

# # shuffle deck
deck = []
while temp:
    randIdx = randint(0, len(temp) - 1)
    deck.append(temp[randIdx])
    del temp[randIdx]

