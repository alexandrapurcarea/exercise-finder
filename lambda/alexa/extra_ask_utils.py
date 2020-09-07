# -*- coding: utf-8 -*-


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
 

def build_success_api_response(returnEntity):
    """Return a formatted API response."""
    # type: (dict[str, str], str) -> dict[str, dict[str, str]]
    
    return { "apiResponse" : returnEntity }