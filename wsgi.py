#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

import app

sys.path.insert(0, abspath(dirname(__file__)))


application = app.configured_app()

if not application.debug:
    import logging
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    application.logger.addHandler(stream_handler)