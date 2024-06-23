import pyCardDeck

my_deck = pyCardDeck.Deck(cards=[1, 2, 3], name='My Awesome Deck')

my_deck.shuffle()



for _ in range(3):
    print(my_deck.draw())