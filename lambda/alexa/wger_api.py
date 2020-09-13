# -*- coding: utf-8 -*-

import requests
import json
import random


# Constants

# This is the only equipment case where capitalization should be removed.
EQUIP_EDGE_CASE = "none (bodyweight exercise)"

# To be considered detailed, a description must have a certain number of characters.
MIN_DESCRIPTION_LENGTH = 50

# Maximum number of entries per search query.
PAGINATION = 100

# Fail ID for search queries.
FAIL_ID = -1

# Only include approved entries in API queries.
APPROVED_STATUS_ID = 2

# English Language ID.
EN_LANG_ID = 2

# Placeholder for ID in a few API endpoints.
ID_PLACEHOLDER = "<id>"

# Wger API Details. 
WGER = {
    "host_name" : "https://wger.de/",
    "api_ext" : "api/v2/",
    "api_category_endpoint" : "exercisecategory/",
    "api_equipment_endpoint" : "equipment/",
    "api_ex_endpoint" : "exercise/",
    "api_ex_info_endpoint" : "exerciseinfo/{}/".format(ID_PLACEHOLDER),
    "api_ex_img_endpoint" : "exerciseimage/{}/thumbnails/".format(ID_PLACEHOLDER)
}

# Default API query header.
DEFAULT_HEADER = {"Accept" : "application/json"}

# Default API query parameters
DEFAULT_PARAMS = {
    "limit" : PAGINATION,
    "status" : APPROVED_STATUS_ID,
    "language" : EN_LANG_ID
}


# Functions


def exercise_finder(category_name, equipment_name):
    """Return an exercise from the Wger API of 
    a certain category and equipment. The a valid exercise must have a detailed description"""
    # type: (str, str) -> Union[dict[str, Any], None]
    
    exercises = [exercise for exercise in exercise_search(category_name, equipment_name) if len(exercise["description"]) > MIN_DESCRIPTION_LENGTH ]
    
    if exercises:
        result = random.choice(exercises)
    else:
        result = None
        
    return result


def exercise_info(exercise_name):
    """Get all the information about an exercise."""
    # type: (str) -> dict[str, Any]

    exercise_id = get_exercise_id(exercise_name)
    url = gen_api_url(
        gen_api_exercise_info_endpoint(str(exercise_id)))

    http_options = {
        "url" : url,
        "headers" : DEFAULT_HEADER,
        "params" : DEFAULT_PARAMS
    }

    return http_get_json(http_options)


# Helpers

def exercise_search(category_name, equipment_name):
    """Return a list of exercises from the Wger API with 
    a certain category ID and equipment ID."""
    # type: (str, str) -> dict[str, Any]

    http_options = {
        "url" : gen_api_url(WGER["api_ex_endpoint"]),
        "headers" : DEFAULT_HEADER,
        "params" : {
            "limit" : PAGINATION,
            "status" : APPROVED_STATUS_ID,
            "language" : EN_LANG_ID,
            "category" : get_category_id(category_name),
            "equipment" : get_equipment_id(equipment_name)
        }
    }

    return http_get_json(http_options)["results"]


def http_get_json(http_options):
    """Return a HTTP get request for JSON content."""
    # type: (dict[str, str])-> dict[str, Any]

    url = http_options["url"]
    headers = http_options["headers"]
    params = http_options["params"]

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code < 200 or response.status_code >= 300:
        response.raise_for_status()

    return response.json()


def gen_api_url(endpoint):
    """Construct a Wger API url given the endpoint"""
    # type: (str) -> str
    return WGER["host_name"] + WGER["api_ext"] + endpoint


def insert_id_in_endpoint(endpoint, id):
    """Replace ID placeholder in the endpoint with ID."""
    # type: (str, int) -> str
    return endpoint.replace("<id>", id)


def gen_api_exercise_info_endpoint(exercise_id):
    """Get the Wger API exercise description endpoint 
    for an exercise ID."""
    # type: (int) -> str
    return insert_id_in_endpoint(WGER["api_ex_info_endpoint"], exercise_id)


def get_id(url, desired_name):
    """Get the ID given the name and the URL listing all entries with their IDs and names."""
    # type: (str) -> int

    http_options = {
        "url" : url,
        "headers" : DEFAULT_HEADER,
        "params" : DEFAULT_PARAMS
    }

    data = http_get_json(http_options)
    result_id = FAIL_ID

    for result in data["results"]:
        if desired_name == result["name"]:
            result_id = result["id"]
            break
        
    if result_id == FAIL_ID:
        if data["next"] is not None:
            result_id = get_id(data["next"], desired_name)
        else:    
            error_message = "Given name did not match any result: {}".format(desired_name)
            raise ValueError(error_message)

    return result_id


def get_exercise_id(exercise_name):
    """Get the exercise ID given the exercise name."""
    # type: (str) -> int

    endpoint = WGER["api_ex_endpoint"] + "?status=" + str(APPROVED_STATUS_ID)

    return get_id(gen_api_url(endpoint), exercise_name)


def get_category_id(category_name):
    """Get the category ID given the category name."""
    # type: (str) -> int
    return get_id(gen_api_url(WGER["api_category_endpoint"]), category_name)


def get_equipment_id(equipment_name):
    """Get the equipment ID given the equipment name."""
    # type: (str) -> int
    return get_id(gen_api_url(WGER["api_equipment_endpoint"]), equipment_name)


def format_equipment(equipment_name):
    """Format the name of the equipment for the API query."""
    # type: (str) -> str

    if (equipment_name == EQUIP_EDGE_CASE):
        result = equipment_name
    else:    
        result = equipment_name.capitalize()
    
    return result