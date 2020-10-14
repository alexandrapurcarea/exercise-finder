# -*- coding: utf-8 -*-

import random
import re

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

NOT_ENOUGH_VALID_ARGUMENTS = (
    "I wasn't able to understand any of what you said. "
    "Please try again, with valid body parts, equipment "
    "and number of exercises."
)

INVALID_NUM_EXERCISES = (
    "The number of exercises for the workout must be between 1 and 10. "
    "Please try again with a valid number."
)

NO_EXERCISES_FOUND = (
    "I was not able to find any exercises matching your criteria. "
    "Try again with different preferences."
)

MISSING_PERMISSIONS = (
    "I do not have the permissions to read and write lists for you. "
    "You must change the skill permissions to allow for this."
)

LIST_FAILURE = (
    "There was an unexpected failure when accessing your lists. Try again some other time."
)

LESS_EXERCISES = "The number of exercises I found was less than you wanted, but "

# Successes

LIST_SUCCESS = "I succesfully created your workout list, check the companion app."

NOT_ALL_QUERIES_MATCHED = (
    "I was only able to find some exercises that matched your body part and equipment preferences, "
    "hence, the workout will include {} exercises."
)

# getDescription API 

def format_description(description):
    """Format the description response such that it sounds natural for Alexa to say."""
    # type: (str) -> str
    
    # Remove newlines.
    html_regex = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    clean_description = re.sub(html_regex, ' ', description)
    
    return clean_description


# Exceptions

# General exception message
EXCEPTION_MSG = "Please try again."

# If no exercise was found by the exercise finder.
EXERCISE_NOT_FOUND = "no exercise"

# Description if not exercise was found.
NOT_FOUND_DESCRIPTION = "Try to find an exercise with different equipment or body part."
