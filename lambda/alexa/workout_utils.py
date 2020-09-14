# -*- coding: utf-8 -*-

from alexa import wger_api

import random


# Minimum number of exercises in a workout.
MIN_WORKOUT_NUM = 1
# Maximum number of exercises in a workout.
MAX_WORKOUT_NUM = 10


# Functions

def create_workout_queries(category_list, equipment_list, number_of_exercise):
    """Create a workout list given the body parts and equipment that 
    should be incorporated and the number of exercises."""
    # type: (list, list, int) -> list

    if (not category_list) or (not equipment_list):
        error_msg = "Empty lists given\n categories = {}\n equipment = {}".format(category_list, equipment_list)
        raise ValueError(error_msg)
    elif number_of_exercise < MIN_WORKOUT_NUM or number_of_exercise > MAX_WORKOUT_NUM:
        error_msg = "Number of exercises outside of bounds: {}".format(number_of_exercise)
        raise ValueError(error_msg)

    workout_queries = []

    for i in range(number_of_exercise):
        category = random.choice(category_list).capitalize()
        equipment = wger_api.format_equipment(
            random.choice(equipment_list))

        workout_queries.append( (category, equipment) )
    
    return workout_queries


def create_workout(workout_queries):
    """Creates a workout of exercises given the exercise query for each workout.
        If the query returns no exercise, the result is omitted from the list."""
    # type: (list) -> list

    workout = []

    for (category, equipment) in workout_queries:
        exercise = wger_api.exercise_finder(category, equipment)

        if exercise is not None:
            workout.append(exercise["name"])

    return workout


# Helpers

def remove_all_None(a_list):
    """Remove all None values from a list."""
    # type: (list) -> list
    return [item for item in a_list if item is not None]


def find_list(list_name, alexa_lists):
    """Check if the user has a list with the given list name. 
    Return true, if the list is found, otherwise false."""
    # type: (str, list) -> bool

    for alexa_list in alexa_lists:
        if alexa_list.name == list_name:
            return True  

    return False


def get_list_id(list_name, alexa_lists):
    """Find a list id for the corresponding list name. 
    If none is found, return None."""
    # type: (str, list) -> Union[str, None]

    for alexa_list in alexa_lists:
        if alexa_list.name == list_name:
            return alexa_list.list_id
    
    return None
