# -*- coding: utf-8 -*-
import logging
import os
import pytest


def pytest_configure(config):
    os.environ["TESTING"] = "1"
    logging.getLogger("watchdog").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
