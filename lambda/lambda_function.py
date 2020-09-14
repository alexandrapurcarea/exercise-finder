# -*- coding: utf-8 -*-

from alexa import extra_ask_utils, workout_utils, wger_api, messages

import logging
import json

from ask_sdk_model import Response

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import ( 
    AbstractRequestHandler, 
    AbstractExceptionHandler, 
    AbstractResponseInterceptor, 
    AbstractRequestInterceptor 
)


# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Alexa List Management API

def createWorkoutList(service_client_fact, workout):
    """Attempt to create a workout list, and relay the success of the operation to the user."""
    # type: (ServiceClientFactory, list[str]) -> str

    result = ""

    try:
        list_management_service = service_client_fact.get_list_management_service()
        lists_metadata = list_management_service.get_lists_metadata().lists

        logger.info("Lists metadata: {}".format(lists_metadata))

        # Remove the previous workout list
        if (workout_utils.find_list(messages.LIST_NAME, lists_metadata)):
            old_list_id = workout_utils.get_list_id(messages.LIST_NAME, lists_metadata)
            list_management_service.delete_list(old_list_id)
            
        list_management_service.create_list(messages.CREATE_LIST_REQUEST)
        lists_metadata = list_management_service.get_lists_metadata().lists
        new_list_id = workout_utils.get_list_id(messages.LIST_NAME, lists_metadata)

        for exercise in workout:
            item_request = {
                "value": exercise,
                "status": messages.STATE
            }
            
            list_management_service.create_list_item(new_list_id, item_request)
            logger.info("Exercise added to list: {}".format(exercise))
        
        result = messages.LIST_SUCCESS
    except Exception as e:
        logger.info(str(e))
        result = messages.LIST_FAILURE
    
    return result


# Custom Request Handlers

class GetRecommendationAPIHandler(AbstractRequestHandler):
    """Handler for getRecommendation API requests."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            ask_utils.is_request_type("Dialog.API.Invoked")(handler_input) 
                and extra_ask_utils.is_api_request_name("getRecommendation")(handler_input)
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetRecommendationAPIHandler")
        
        api_request = handler_input.request_envelope.request.api_request
        
        body_part = extra_ask_utils.resolve_entity(api_request.slots, "bodyPart")
        equipment = extra_ask_utils.resolve_entity(api_request.slots, "equipment")
        
        recommendation_entity = {}
        if (body_part is not None) and (equipment is not None):
            recommendation_entity["bodyPart"] = body_part.capitalize()
            recommendation_entity["equipment"] = wger_api.format_equipment(equipment)
            
            exercise = wger_api.exercise_finder(
                recommendation_entity["bodyPart"], 
                recommendation_entity["equipment"]
            )
            logger.info("Response from wger API: {}".format(exercise))
            
            if exercise is None:
                exercise_name = messages.EXERCISE_NOT_FOUND
            else:
                exercise_name = exercise["name"]
            
            recommendation_entity["exerciseName"] = exercise_name
        else:
            recommendation_entity["bodyPart"] = body_part
            recommendation_entity["equipment"] = equipment
            recommendation_entity["exerciseName"] = messages.EXERCISE_NOT_FOUND    
            
            logger.info("Faulty Response: {}".format(recommendation_entity))
            
            
        response = extra_ask_utils.build_success_api_response(recommendation_entity)
        return response


class GetDescriptionAPIHandler(AbstractRequestHandler):
    """Handler for getDescription API requests."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            ask_utils.is_request_type("Dialog.API.Invoked")(handler_input) 
                and extra_ask_utils.is_api_request_name("getDescription")(handler_input)
        )
         
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetDescriptionAPIHandler")
        
        recommendation_result = handler_input.request_envelope.request.api_request.arguments['recommendationResult']
        exercise_name = recommendation_result["exerciseName"]
        
        if (exercise_name == messages.EXERCISE_NOT_FOUND) or (exercise_name is None):
            exercise_description = messages.NOT_FOUND_DESCRIPTION 
        else: 
            exercise_description = messages.format_description(wger_api.exercise_info(exercise_name)["description"])
            logger.info("Response from wger API: {}".format(exercise_description))

        description_entity = {"description" : exercise_description}
        response = extra_ask_utils.build_success_api_response(description_entity)
        return response


class createWorkoutAPIHandler(AbstractRequestHandler):
    """Handler for createWorkout API requests. TODO"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (
            ask_utils.is_request_type("Dialog.API.Invoked")(handler_input) 
                and extra_ask_utils.is_api_request_name("createWorkout")(handler_input)
        )

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In createWorkoutAPIHandler")
        
        # Alexa conversations

        response = ""
        api_request = handler_input.request_envelope.request.api_request
        
        body_part_i = extra_ask_utils.resolve_entity(api_request.slots, "bodyPart_I")
        body_part_ii = extra_ask_utils.resolve_entity(api_request.slots, "bodyPart_II")
        body_part_iii = extra_ask_utils.resolve_entity(api_request.slots, "bodyPart_III")
        equipment_i = extra_ask_utils.resolve_entity(api_request.slots, "equipment_I")
        equipment_ii = extra_ask_utils.resolve_entity(api_request.slots, "equipment_II")
        equipment_iii = extra_ask_utils.resolve_entity(api_request.slots, "equipment_III")
        number_of_exercises = api_request.arguments["numberOfExs"]
        
        body_parts = workout_utils.remove_all_None([body_part_i, body_part_ii, body_part_iii])
        equipment = workout_utils.remove_all_None([equipment_i, equipment_ii, equipment_iii])

        # wger API

        if (not body_parts) or (not equipment) or (number_of_exercises is None):
            return extra_ask_utils.createWorkout_response(messages.NOT_ENOUGH_VALID_ARGUMENTS)
        else:
            # If the number of exercises exists, it should be converted to an int.
            number_of_exercises = int(number_of_exercises)  

        if (number_of_exercises < workout_utils.MIN_WORKOUT_NUM) or (number_of_exercises > workout_utils.MAX_WORKOUT_NUM):
            return extra_ask_utils.createWorkout_response(messages.INVALID_NUM_OF_EXERCISES)
        
        exercise_queries = workout_utils.create_workout_queries(body_parts, equipment, number_of_exercises)
        workout = workout_utils.create_workout(exercise_queries)
        logger.info("Response from wger API: {}".format(workout))

        if not workout:
            return extra_ask_utils.createWorkout_response(messages.NO_EXERCISES_FOUND)

        elif (len(workout) != len(exercise_queries)):
            response += messages.NOT_ALL_QUERIES_MATCHED.format(
                str(len(workout)))
        
        # List Management API

        req_envelope = handler_input.request_envelope
        if not (req_envelope.context.system.user.permissions and
                req_envelope.context.system.api_access_token):
            return extra_ask_utils.createWorkout_response(messages.MISSING_PERMISSIONS)

        response += createWorkoutList(handler_input.service_client_factory, workout)
        return extra_ask_utils.createWorkout_response(response)


# Standard Request Handler
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        logger.info("Session ended with reason: {}".format(
            handler_input.request_envelope.request.reason))

        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors."""

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        return (
            handler_input.response_builder
                .speak(messages.EXCEPTION_MSG)
                .ask(messages.EXCEPTION_MSG)
                .response
        )


# Request and Response Loggers

class RequestLogger(AbstractRequestInterceptor):
    """Log the request envelope."""
    
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.info('Request recieved: {}'.format(handler_input.request_envelope))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info('Response generated: {}'.format(response))


# Skillbuilder 
sb = CustomSkillBuilder(api_client=DefaultApiClient())

# Custom 
sb.add_request_handler(createWorkoutAPIHandler())
sb.add_request_handler(GetRecommendationAPIHandler())
sb.add_request_handler(GetDescriptionAPIHandler())

# Standard
sb.add_request_handler(SessionEndedRequestHandler())

# Exceptions
sb.add_exception_handler(CatchAllExceptionHandler())

# Loggers
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Lambda Handler
lambda_handler = sb.lambda_handler()