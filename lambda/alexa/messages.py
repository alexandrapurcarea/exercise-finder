# -*- coding: utf-8 -*-

import random


# Welcome

WELCOME_MSG_START = ("Welcome to Exercise Finder! " 
                     "Find an exercise which meets your requirements. ")

WELCOME_MSG_MIDDLES = [ 
    "You can specify by the body part or muscle you want to use.",
    "I can take into account the equipment you have available. ",
    "Choose based on the muscle or body part you want to strengthen. ",
    "Only have certain types of equipment? no problem."
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
HELP_MSG = ("I can help you find an exercise which matches your preferences, "
            "with respect to body part or muscle and equipment.") 

# Fallback
FALLBACK_MSG = "Sorry, I can't do that. However, {}".format(HELP_MSG)

# Exit

EXIT_MSG_START = ("Thank you for using exercise finder. ")

EXIT_MSG_ENDS = [
    "Practice makes perfect!"
    "The clock is ticking. Are you becoming the person you want to be?"
    "There are no shortcuts to any place worth going."
    "The secret of getting ahead is getting started."
    "What hurts today makes you stronger tomorrow."
    "No pain, no gain."
    "Your body can stand almost anything. It’s your mind that you have to convince."
    "Good things come to those who sweat."
    "What seems impossible today will one day become your warm-up."
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


# getDescription API 

# Length of pauses between steps.
PAUSE_DURATION = 1

def format_description(description):
    """Format the description response such that it sounds natural for Alexa to say."""
    # type: (str) -> str

    # Remove newlines from Alexa response.
    description = description.replace("\n", " ")

    # Add pauses to allow user to process instructions.
    description = description.replace(".", '<break time="{}s"/>.'.format(str(PAUSE_DURATION)))
    
    return description