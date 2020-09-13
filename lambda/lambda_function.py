# -*- coding: utf-8 -*-

from alexa import extra_ask_utils, wger_api, messages

import logging
import json

from ask_sdk_model import Response

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import SkillBuilder
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
            logger.info("Response from Wger API: {}".format(exercise))
            
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
        api_response = "I don't know much about {}.".format(exercise_name)
        
        description_entity = {}
        if (exercise_name == messages.EXERCISE_NOT_FOUND) or (exercise_name is None):
            exercise_description = messages.NOT_FOUND_DESCRIPTION 
        else: 
            exercise_description = messages.format_description(
                wger_api.exercise_info(exercise_name)["description"]
            )
            logger.info("Response from Wger API: {}".format(api_response))

        description_entity["description"] = exercise_description
        response = extra_ask_utils.build_success_api_response(description_entity)
        return response


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
        logger.info('Request recieved: {}'.format(handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the response envelope."""
    
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.info('Response generated: {}'.format(response))


# Skillbuilder 
sb = SkillBuilder()

# Custom 
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