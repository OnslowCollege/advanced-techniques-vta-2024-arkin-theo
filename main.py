"""
Main.

Created by: NAME
Date: DATE
"""

from random import shuffle
import pandas as PD
import remi.gui as GUI
from remi import App, start


class BlackJackApp(App):

    NMB_DECKS = 8
    DECKS_BF_RS = 4

    def __init__(self, *args) -> None:
        import os
        abs_path: str = os.path.abspath(__file__)
        dir_name: str = os.path.dirname(abs_path)
        res_path: str = os.path.join(dir_name, "res")

        # Create cards
        deck: list = []
        for i in range(52):
            



    def main(self) -> GUI.Widget:
        return GUI.HBox

start(BlackJackApp)