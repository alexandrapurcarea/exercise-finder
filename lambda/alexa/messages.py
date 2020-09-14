# -*- coding: utf-8 -*-

import random

# createWorkout API

# The name of the list being created.
LIST_NAME = "Workout"

# The state of the list being created.
STATE = "active"

# The request for creating the list.
CREATE_LIST_REQUEST = {
    "name": LIST_NAME,
    "state": STATE
}


# Fails

CREATEWORKOUT_EXCEPTION_START = "Sorry, I did not create a workout list."

NOT_ENOUGH_VALID_ARGUMENTS = CREATEWORKOUT_EXCEPTION_START + (
    "I wasn't able to understand any of what you said. "
    "Please try again, with valid body parts, equipment "
    "and number of exercises."
)

INVALID_NUM_EXERCISES = CREATEWORKOUT_EXCEPTION_START + (
    "The number of exercises for the workout must be between 1 and 10. "
    "Please try again with a valid number."
)

NO_EXERCISES_FOUND = CREATEWORKOUT_EXCEPTION_START + (
    "I was not able to find any exercises matching your criteria. "
    "Try again with different preferences."
)

MISSING_PERMISSIONS = CREATEWORKOUT_EXCEPTION_START + (
    "I do not have the permissions to read and write lists for you. "
    "You must change the skill permissions to allow for this."
)

LIST_FAILURE = CREATEWORKOUT_EXCEPTION_START + (
    "There was an unexpected failure when accessing your lists. Try again some other time."
)

# Successes

LIST_SUCCESS = "I succesfully created your workout list, check the companion app."

NOT_ALL_QUERIES_MATCHED = (
    "I was only able to find some exercises that matched your body part and equipment preferences, "
    "hence, the workout will include {} exercises."
)

# getDescription API 

NEWLINE = "\n"

# HTML paragraph code.
HTML_PARAGRAPH_START = "<p>"
HTML_PARAGRAPH_END = "</p>"
HTML_SOMETHING_START = "<ol>"
HTML_SOMETHING_END = "</ol>"
HTML_SOMETHING_2_START = "<li>"
HTML_SOMETHING_2_END = "</li>"

def format_description(description):
    """Format the description response such that it sounds natural for Alexa to say."""
    # type: (str) -> str
    
    # Remove newlines.
    description = description.replace(NEWLINE, " ")
    
    # Removes HTML
    description = description.replace(HTML_PARAGRAPH_START, " ")
    description = description.replace(HTML_PARAGRAPH_END, " ")
    description = description.replace(HTML_SOMETHING_START, " ")
    description = description.replace(HTML_SOMETHING_END, " ")
    description = description.replace(HTML_SOMETHING_2_START, " ")
    description = description.replace(HTML_SOMETHING_2_END, " ")
    
    return description


# Exceptions

# General exception message
EXCEPTION_MSG = "Sorry, I had trouble doing what you asked. Please try again."

# If no exercise was found by the exercise finder.
EXERCISE_NOT_FOUND = "no exercise"

# Description if not exercise was found.
NOT_FOUND_DESCRIPTION = "Sorry, I did not find any exercise matching your preferences. Try to find an exercise with different equipment or body part."