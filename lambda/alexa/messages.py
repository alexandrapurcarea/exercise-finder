# -*- coding: utf-8 -*-

import random


# Welcome

WELCOME_MSG_START = ("Welcome to Viva Voce! " 
                    "Review your topics with flashcards, or ")

WELCOME_MSG_MIDDLES = [ 
    "edit your decks by adding new cards.",
    "perfect a deck with a few new additions. ",
    "create completely new flashcard decks. ",
    "learn a new topic by creating a new deck. ",
    "remove your unused flashcard decks. ",
    "get rid of one of those unused decks. ",
    ]

WELCOME_MSG_END = "What do you want to do?"


def welcome_message():
    """Create a welcome message."""
    # type : (HandlerInput) -> str
    return (
        WELCOME_MSG_START 
        + random.choice(WELCOME_MSG_MIDDLES) 
        + WELCOME_MSG_END
    )


# Help
HELP_MSG = ("I can quiz you on a deck you have created, "
             "edit it with new cards, or"
             "remove it from your library. "
             "If you want to learn something new, "
             "I can help you create a completely new deck. "
             "Also, if you have forgotten the name of your decks, "
             "just ask, and I'll give you a quick rundown.") 

# Fallback
FALLBACK_MSG = "Sorry, I can't do that. However, {}".format(HELP_MSG)

# Exit

EXIT_MSG_START = ("Thank you for using Viva Voce. ")

EXIT_MSG_ENDS = [
    "Practice makes perfect!"
    "Genius is one percent inspiration, ninety-nine percent perspiration!"
    "There are no shortcuts to any place worth going."
    "The secret of getting ahead is getting started."
    "Till next time"
    "See you again!"
    "Goodbye!"
    ]            


def exit_message():
    "Create an exit message."
    # type : (HandlerInput) -> str 
    return (
        EXIT_MSG_START 
        + random.choice(EXIT_MSG_ENDS) 
    )


# Exception
EXCEPTION_MSG = "Sorry, I had trouble doing what you asked. Please try again."