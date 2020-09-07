# -*- coding: utf-8 -*-

import pytest
from alexa import wger_api


def test_exercise_finder():
    category_name = "Back"
    category_id = 12
    equipment_name = "Barbell"
    equipment_id = 1
    result = wger_api.exercise_finder(category_name, equipment_name)

    if isinstance(result["category"], list):
        assert category_id in result["category"]
    else:
        assert result["category"] == category_id
    
    if isinstance(result["equipment"], list):
        equipment_id in result["equipment"]
    else:
        assert result["equipment"] == wger_api.get_equipment_id(equipment_name)


def test_exercise_info():
    exercise_name = "Crunches"
    result = wger_api.exercise_info(exercise_name)

    assert result["name"] == exercise_name