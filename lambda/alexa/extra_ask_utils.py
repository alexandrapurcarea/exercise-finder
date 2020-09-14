# -*- coding: utf-8 -*-

from ask_sdk_model.slu.entityresolution import StatusCode


# General

def is_api_request_name(name):
    """A predicate function returning a boolean, when name matches the
    name in API request name."""
    # type: (str) -> Callable[[HandlerInput], bool]

    def can_handle_wrapper(handler_input):
        # type: (HandlerInput) -> bool
        return (
            handler_input.request_envelope.request.api_request.name 
                == name
        )
        
    return can_handle_wrapper


def resolve_entity(resolvedEntity, slot):
    """Resolve the slot name from the API request resolutions."""
    # type: (ResolvedEntity, str) -> str
    
    value = None
    
    try:
        erAuthorityResolution = resolvedEntity[slot].resolutions.resolutions_per_authority[0]
        
        if (erAuthorityResolution.status.code == StatusCode.ER_SUCCESS_MATCH):
            value = erAuthorityResolution.values[0].value.name
            
    except (AttributeError, ValueError, KeyError, IndexError, TypeError) as e:
        print("Couldn't resolve {} from slots: {}".format(slot, resolvedEntity))
        print(str(e))
        
    return value   


def build_success_api_response(returnEntity):
    """Return a formatted API response."""
    # type: (dict[str, str], str) -> dict[str, dict[str, str]]
    return { "apiResponse" : returnEntity }


# creatWorkout API

def createWorkout_response(success_message):
    """Create a response for the createWorkout API, given the message you want to relay """
    # type: (str) -> dict[str, str]

    workout_entity = {"successMessage" : success_message}
    response = build_success_api_response(workout_entity) 
    return response