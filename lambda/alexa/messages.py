# -*- coding: utf-8 -*-

import random

    
# Exception
EXCEPTION_MSG = "Sorry, I had trouble doing what you asked. Please try again."


# getDescription API 

NEWLINE = "\n"

# Signifies the end of a step.
STEP_END = "."

# Length of pauses between steps.
PAUSE_DURATION = 1

# Pause formatting in SSML.
PAUSE = '<break time="{}s"/>'.format(str(PAUSE_DURATION))

def format_description(description):
    """Format the description response such that it sounds natural for Alexa to say."""
    # type: (str) -> str

    # Remove newlines from Alexa response.
    description = description.replace(NEWLINE, " ")

    # Add pauses to allow user to process instructions.
    description = description.replace(STEP_END, PAUSE + STEP_END)
    
    return description