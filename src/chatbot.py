#!/bin/python

from extract_mod import extract
from random import choice

class trash_bot():
    """Fuck you NOOOOB!"""

    def __init__(self, chat_file):
        """Constructor"""

        self.vocabulary = extract(chat_file,selected_columns=[1])

    def talk(self):
        """Calmly says something"""
        return choice(self.vocabulary)["key"]

    def shout(self):
        """NOW I'M MAD"""
        return choice(self.vocabulary)["key"].upper()
