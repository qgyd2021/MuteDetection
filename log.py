#!/usr/bin/python3
# -*- coding: utf-8 -*-
import logging
from logging.handlers import TimedRotatingFileHandler
import os


def setup(log_directory: str):
    fmt = "%(asctime)s - %(name)s - %(levelname)s  %(filename)s:%(lineno)d >  %(message)s"

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(fmt))

    # main
    main_logger = logging.getLogger("main")
    main_logger.addHandler(stream_handler)
    main_info_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, "main.log"),
        encoding="utf-8",
        when="midnight", 
        interval=1, 
        backupCount=30
    )
    main_info_file_handler.setLevel(logging.INFO)
    main_info_file_handler.setFormatter(logging.Formatter(fmt))
    main_logger.addHandler(main_info_file_handler)

    # http
    http_logger = logging.getLogger("http")
    http_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, "http.log"),
        encoding='utf-8',
        when="midnight",
        interval=1,
        backupCount=30
    )
    http_file_handler.setLevel(logging.DEBUG)
    http_file_handler.setFormatter(logging.Formatter(fmt))
    http_logger.addHandler(http_file_handler)

    # api
    api_logger = logging.getLogger("api")
    api_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, "api.log"),
        encoding='utf-8',
        when="midnight",
        interval=1,
        backupCount=30
    )
    api_file_handler.setLevel(logging.DEBUG)
    api_file_handler.setFormatter(logging.Formatter(fmt))
    api_logger.addHandler(api_file_handler)

    # alarm
    alarm_logger = logging.getLogger("alarm")
    alarm_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, "alarm.log"),
        encoding="utf-8",
        when="midnight",
        interval=1,
        backupCount=30
    )
    alarm_file_handler.setLevel(logging.DEBUG)
    alarm_file_handler.setFormatter(logging.Formatter(fmt))
    alarm_logger.addHandler(alarm_file_handler)

    debug_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, "debug.log"),
        encoding="utf-8",
        when="D",
        interval=1,
        backupCount=7
    )
    debug_file_handler.setLevel(logging.DEBUG)
    debug_file_handler.setFormatter(logging.Formatter(fmt))

    info_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, "info.log"),
        encoding="utf-8",
        when="D",
        interval=1,
        backupCount=7
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(fmt))

    error_file_handler = TimedRotatingFileHandler(
        filename=os.path.join(log_directory, "error.log"),
        encoding="utf-8",
        when="D",
        interval=1,
        backupCount=7
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(logging.Formatter(fmt))

    logging.basicConfig(
        level=logging.DEBUG,
        datefmt="%a, %d %b %Y %H:%M:%S",
        handlers=[
            debug_file_handler,
            info_file_handler,
            error_file_handler,
        ]
    )


if __name__ == "__main__":
    pass
