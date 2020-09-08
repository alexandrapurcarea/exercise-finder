# -*- coding: utf-8 -*-

from alexa import extra_ask_utils, wger_api, messages

import logging
import json

from ask_sdk_model import Response
from ask_sdk_model.slu.entityresolution import StatusCode

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.serialize import DefaultSerializer
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

class getRecommendationAPIHandler(AbstractRequestHandler):
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
        
        apiRequest = handler_input.request_envelope.request.api_request
        
        bodyPart = resolveEntity(apiRequest.slots, "bodyPart").capitalize()
        equipment = resolveEntity(apiRequest.slots, "equipment").capitalize()
        
        recommendationEntity = {}
        if (bodyPart != None) and (equipment != None):
            recommendationEntity["bodyPart"] = bodyPart
            recommendationEntity["equipment"] = equipment

            api_response_exercise = wger_api.exercise_finder(bodyPart, equipment)
            logger.info("Response from Wger API: {}".format(api_response_exercise))

            recommendationEntity["exerciseName"] = api_response_exercise["name"]
            
        response = extra_ask_utils.build_success_api_response(recommendationEntity)
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
        
        recommendationResult = handler_input.request_envelope.request.api_request.arguments['recommendationResult']
        
        api_response = "I don't know much about {}.".format(recommendationResult["name"])
        
        exerciseName = recommendationResult["exerciseName"]
        
        descriptionEntity = {}
        if (exerciseName != None):
            api_response = wger_api.exercise_info(exercise_name)
            logger.info("Response from Wger API: {}".format(api_response))
                
            descriptionEntity["description"] = messages.format_description(api_response["description"])
        
        response = extra_ask_utils.build_success_api_response(descriptionEntity)
        return response


# Standard Request Handlers

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")

        speak_output = messages.welcome_message()
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.attributes_manager.session_attributes = {}

        return (
            handler_input.response_builder
                .speak(messages.HELP_MSG)
                .ask(messages.HELP_MSG)
                .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for handling fallback intent.

     2018-May-01: AMAZON.FallackIntent is only currently available in
     en-US locale. This handler will not be triggered except in that
     locale, so it can be safely deployed for any locale.
     """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        return (
            handler_input.response_builder
                .speak(messages.FALLBACK_MSG)
                .ask(messages.HELP_MSG)
                .response
        )


class ExitIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ExitIntentHandler")

        speak_output = messages.exit_message()
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_should_end_session(True)
                .response
        )


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


class RepeatHandler(AbstractRequestHandler):
    """Handler for repeating responses."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In RepeatHandler")

        attr = handler_input.attributes_manager.session_attributes

        if "recent_response" in attr:
            cached_response_str = json.dumps(attr["recent_response"])
            cached_response = DefaultSerializer().deserialize(cached_response_str, Response)

            return cached_response
        else:
            return ( 
                handler_input.response_builder
                    .speak(messages.FALLBACK_MSG)
                    .ask(messages.HELP_MSG)
            )


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


# Cache Interceptor
class CacheResponseInterceptor(AbstractResponseInterceptor):
    """Cache the response sent to the user to allow for repition."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr["recent_response"] = response


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


# Utilities


def resolveEntity(resolvedEntity, slot):
    """Resolve the slot name from the API request resolutions."""
    # type: (ResolvedEntity, str) -> str
    
    value = None
    
    try:
        erAuthorityResolution = resolvedEntity[slot].resolutions.resolutions_per_authority[0]
        
        if (erAuthorityResolution.status.code == StatusCode.ER_SUCCESS_MATCH):
            value = erAuthorityResolution.values[0].value.name
            
    except (AttributeError, ValueError, KeyError, IndexError, TypeError) as e:
        logger.info("Couldn't resolve {} from slots: {}".format(slot, resolvedEntity))
        logger.info(str(e))
        
    return value   


# Skillbuilder 
sb = SkillBuilder()

# Custom 
sb.add_request_handler(getRecommendationAPIHandler())
sb.add_request_handler(GetDescriptionAPIHandler)

# Standard
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(RepeatHandler())

# Exceptions
sb.add_exception_handler(CatchAllExceptionHandler())

# Caching
sb.add_global_response_interceptor(CacheResponseInterceptor())

# Loggers
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Lambda Handler
lambda_handler = sb.lambda_handler()