from random import randrange

# Create a deck of cards format: [[suit, value], [suit, value], ...]
temp = [[suit, value] for suit in ["Clubs", "Hearts", "Spades", "Diamonds"] for value in range(1, 14)]

# shuffle deck
deck = temp
while temp:
    randIdx = randrange(1, len(deck))
    deck.append(temp[randIdx])

print(deck)