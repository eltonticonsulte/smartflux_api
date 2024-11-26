# -*- coding: utf-8 -*-
import logging
import os
from datetime import datetime
from .logger import LoggerConfig


def default_log(dir_log: str = "log") -> None:

    version = os.getenv("SMARTFLUX_VERSION", "0.0.0")
    version = version.replace(".", "-")
    timestamp = datetime.now().strftime("%Y-%m-%d")

    name_log = f"smartflux_{timestamp}_v{version}.log"
    path_log = os.path.join(dir_log, name_log)

    level = logging.INFO
    if os.environ.get("LOG_LEVEL") == "DEBUG":
        level = logging.DEBUG

    LoggerConfig(
        console_level=level,
        file_level=logging.DEBUG,
        path_logger=path_log,
    )
