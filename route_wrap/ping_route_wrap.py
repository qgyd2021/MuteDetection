#!/usr/bin/python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import time
import traceback
import uuid

from aiohttp import web

from exception import ExpectedError

main_logger = logging.getLogger("main")


def ping_route_wrap(f):
    if not asyncio.iscoroutinefunction(f):
        raise AssertionError("f must be coroutine.")

    async def inner(*args, **kwargs):
        begin = time.time()
        try:
            ext = await f(*args, **kwargs)
            response = {
                "retCode": 0,
                "retMsg": "success",
                "responseID": str(uuid.uuid4()),
                "ext": ext,
            }
            status_code = 200
        except ExpectedError as e:
            response = {
                "retCode": e.status_code,
                "retMsg": e.message,
                "responseID": str(uuid.uuid4()),
                "detail": e.detail,
                "traceback": e.traceback,
            }
            status_code = 400
        except Exception as e:
            response = {
                "retCode": 1,
                "retMsg": str(e),
                "responseID": str(uuid.uuid4()),
                "detail": None,
                "traceback": traceback.format_exc(),
            }
            status_code = 500

        cost = time.time() - begin
        response["time_cost"] = round(cost, 4)

        return web.json_response(response, status=status_code)
    return inner
