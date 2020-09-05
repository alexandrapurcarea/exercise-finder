# -*- coding: utf-8 -*-

from alexa import messages

import logging
import json

from ask_sdk_model import Response

import ask_sdk_core.utils as ask_utils

from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import ( AbstractRequestHandler
                                             , AbstractExceptionHandler
                                             , AbstractResponseInterceptor
                                             , AbstractRequestInterceptor )


# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


# Debugging Handler
class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
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


# Skillbuilder 
sb = SkillBuilder()

# Standard
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(ExitIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(RepeatHandler())

# make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers
sb.add_request_handler(IntentReflectorHandler())

# Exceptions
sb.add_exception_handler(CatchAllExceptionHandler())

# Caching
sb.add_global_response_interceptor(CacheResponseInterceptor())

# Loggers
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Lambda Handler
lambda_handler = sb.lambda_handler()