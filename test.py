import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None
        
# Create a new deck
deck = Deck()

decks_list: list = [deck for _ in range(6)]

# Shuffle the deck
for deck in decks_list:
    deck.shuffle()

print(len(decks_list))

# Deal a card
card = deck.deal()
print(card.rank)

print(len(deck.cards))


# for cards in deck.cards:
#     print(cards.rank)
