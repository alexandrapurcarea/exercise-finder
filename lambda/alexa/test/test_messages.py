# -*- coding: utf-8 -*-

import pytest
from alexa import messages


def test_format_description():
    description = "- Hello world.\n I <p>dunno man</p>."
    result = messages.format_description(description) 

    assert result == "- Hello world.  I  dunno man ." 