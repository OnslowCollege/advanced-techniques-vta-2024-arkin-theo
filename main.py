"""
Main.

Created by: NAME
Date: DATE
"""

from random import shuffle
import pandas as PD
import remi.gui as GUI
from remi import App, start

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def __init__(self, nmb_decks):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks for _ in range(nmb_decks)]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None


class BlackJackApp(App):

    NMB_DECKS = 8
    DECKS_BF_RS = 4


    def __init__(self, *args) -> None:
        import os
        abs_path: str = os.path.abspath(__file__)
        dir_name: str = os.path.dirname(abs_path)
        res_path: str = os.path.join(dir_name, "res")

        # Create dealer's shoe
        d_shoe = Deck(self.NMB_DECKS)

        player_hand = 



    def main(self) -> GUI.Widget:
        return GUI.HBox

start(BlackJackApp)