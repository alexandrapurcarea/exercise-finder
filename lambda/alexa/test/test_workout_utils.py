# -*- coding: utf-8 -*-

import pytest
from alexa import workout_utils, wger_api

# Constants

BODY_PARTS = ["arms", "shoulders"]

EQUIPMENTS = ["dumbbell", "bench", wger_api.EQUIP_EDGE_CASE]

NUM_OF_EXERCISES = 5

QUERIES = workout_utils.create_workout_queries(BODY_PARTS, EQUIPMENTS, NUM_OF_EXERCISES)


# Tests

def test_create_workout_queries():
    length_of_valid_items = len(
        [ 
            1 for (bodyPart, equipment) in QUERIES 
            if (bodyPart.lower() in BODY_PARTS) 
                and (equipment.lower() in EQUIPMENTS)
        ]
    )

    assert length_of_valid_items == NUM_OF_EXERCISES


def test_create_workout():
    workout = workout_utils.create_workout(QUERIES)

    length_of_valid_items = len(
        [
            1 for exercise in workout
            if wger_api.exercise_info(exercise)["name"] == exercise
        ]
    )

    assert length_of_valid_items == len(workout)
