# -*- coding: utf-8 -*-

from alexa import wger_api

import random


# Minimum number of exercises in a workout.
MIN_WORKOUT_NUM = 1
# Maximum number of exercises in a workout.
MAX_WORKOUT_NUM = 10


def create_workout_queries(category_list, equipment_list, number_of_exercise):
    """Create a workout list given the body parts and equipment that 
    should be incorporated and the number of exercises."""
    # type: (list, list, int) -> list

    category_list = remove_all_None(category_list)
    equipment_list = remove_all_None(equipment_list)

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
    The returned bool is true if the workout was succesfully created, false otherwise.
    Assumes that all queries are correctly formatted.
    """
    # type: (list) -> (list, bool) 

    workout = []

    for (category, equipment) in workout_queries:
        exercise = wger_api.exercise_finder(category, equipment)["name"]

        if exercise:
            workout.append(exercise)

    return (workout, len(workout) == len(workout_queries))


# Helper

def remove_all_None(a_list):
    """Remove all None values from a list."""
    # type: (list) -> list
    return [item for item in a_list if item is not None]
