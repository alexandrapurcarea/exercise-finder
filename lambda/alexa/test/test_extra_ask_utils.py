# -*- coding: utf-8 -*-

import pytest
from alexa import extra_ask_utils

def test_build_success_api_response():
    api_response = {"hello" : "goodbye"}
    assert extra_ask_utils.build_success_api_response(api_response)["apiResponse"] == api_response