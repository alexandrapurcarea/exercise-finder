# -*- coding: utf-8 -*-

import pytest
from alexa import messages


def test_welcome_message():
    sample = messages.welcome_message()

    middle_start_pos = len(messages.WELCOME_MSG_START)
    middle_end_pos   = - len(messages.WELCOME_MSG_END)

    message_start  = sample[ : middle_start_pos] 
    message_middle = sample[ middle_start_pos : middle_end_pos]
    message_end    = sample[ middle_start_pos + len(message_middle) : ]

    assert message_start == messages.WELCOME_MSG_START
    assert message_middle in messages.WELCOME_MSG_MIDDLES
    assert message_end == messages.WELCOME_MSG_END


def test_exit_message():
    sample = messages.exit_message()

    start_length = len(messages.EXIT_MSG_START)

    message_start = sample[ : start_length]
    message_end   = sample[ start_length : ]

    assert message_start == messages.EXIT_MSG_START
    assert message_end in messages.EXIT_MSG_ENDS

