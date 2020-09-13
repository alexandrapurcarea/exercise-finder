# -*- coding: utf-8 -*-

import random


# getDescription API 

NEWLINE = "\n"

# Signifies the end of a instruction step.
STEP_END = "."

# Length of pauses between steps in seconds.
PAUSE_DURATION = 1

# Pause formatting in SSML.
PAUSE = '<break time="{}s"/>'.format(str(PAUSE_DURATION))

# Emphasis formatting in SSML.

EMPHASIS_START = "<emphasis level='moderate'>" 

EMPHASIS_END = "</emphasis>"

def format_description(description):
    """Format the description response such that it sounds natural for Alexa to say."""
    # type: (str) -> str

    # Remove newlines from Alexa response.
    description = description.replace(NEWLINE, " ")

    # Add pauses to allow user to process instructions.
    description = description.replace(STEP_END, PAUSE + STEP_END)
    
    # Add emphasis to the instructions
    description = EMPHASIS_START +  description + EMPHASIS_END
    
    return description


# Exceptions

# General exception message
EXCEPTION_MSG = "Sorry, I had trouble doing what you asked. Please try again."

# If no exercise was found by the exercise finder.
EXERCISE_NOT_FOUND = "no exercise"

# Description if not exercise was found.
NOT_FOUND_DESCRIPTION = "Sorry, I did not find any exercise matching your preferences. Try to find an exercise with different equipment or body part."