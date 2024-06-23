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
    def __init__(self, *args) -> None:
        import os
        abs_path: str = os.path.abspath(__file__)
        dir_name: str = os.path.dirname(abs_path)
        res_path: str = os.path.join(dir_name, "res")


    def main(self) -> GUI.Widget:
        return GUI.HBox

start(BlackJackApp)