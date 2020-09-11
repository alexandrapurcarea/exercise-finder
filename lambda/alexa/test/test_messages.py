# -*- coding: utf-8 -*-

import pytest
from alexa import messages


def test_format_description():
    description = "- Hello world.\n I dunno man."
    result = messages.format_description(description) 

    assert result == (
            messages.EMPHASIS_START
            + "- Hello world" 
            + messages.PAUSE 
            + messages.STEP_END 
            + "  I dunno man" 
            + messages.PAUSE 
            + messages.STEP_END
            + messages.EMPHASIS_END
        )