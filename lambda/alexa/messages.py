# -*- coding: utf-8 -*-

import random


# getDescription API 

NEWLINE = "\n"

# HTML paragraph code.
HTML_PARAGRAPH_START = "<p>"
HTML_PARAGRAPH_END = "</p>"


def format_description(description):
    """Format the description response such that it sounds natural for Alexa to say."""
    # type: (str) -> str
    
    # Remove newlines.
    description = description.replace(NEWLINE, " ")
    
    # Removes HTML
    description = description.replace(HTML_PARAGRAPH_START, " ")
    description = description.replace(HTML_PARAGRAPH_END, " ")
    
    return description


# Exceptions

# General exception message
EXCEPTION_MSG = "Sorry, I had trouble doing what you asked. Please try again."

# If no exercise was found by the exercise finder.
EXERCISE_NOT_FOUND = "no exercise"

# Description if not exercise was found.
NOT_FOUND_DESCRIPTION = "Sorry, I did not find any exercise matching your preferences. Try to find an exercise with different equipment or body part."