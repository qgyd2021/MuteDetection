#!/bin/python3
# coding=utf-8
import asyncio
import logging
import os
import time

from aiohttp import web
from aiohttp.web_middlewares import middleware

import settings
import log

log.setup(log_directory=settings.log_directory)

from handlers.on_dialout import handle_on_dialout
from handlers.on_ring import handle_on_ring
from handlers.on_answer import handle_on_answer
from handlers.on_hangup import handle_on_hangup
from handlers.on_pcm import handle_on_pcm
from handlers.ping import ping

from toolbox.logging.misc import json_2_str

http_logger = logging.getLogger("http")
main_logger = logging.getLogger("main")


@middleware
async def authenticate(request, handler):
    token = request.headers.get("Token")

    config = settings.get_config()
    TOKEN = config["service"]["auth_token"]
    if token != TOKEN:
        return web.Response(status=401, text="Invalid Token")
    return await handler(request)


@middleware
async def request_logger(request, handler):
    start_time = time.time()

    url = str(request.url)
    method = request.method
    # print(f"Received request: {method} {url}")

    request_body = await request.json()
    request_body = json_2_str(request_body)
    # request_body = request_body.decode("utf-8")
    # print(f"Request body: {request_body}")

    response = await handler(request)

    http_status = response.status
    response_body = response.text
    # print(f"Response body: {response_body}")

    cost = time.time() - start_time

    # http_logger.info(f"{method}|{url}|{http_status}|{cost:.3f}s|{request_body}|{response_body}")

    return response


def main():
    app = web.Application()

    app.middlewares.append(request_logger)
    app.middlewares.append(authenticate)

    config = settings.get_config()
    app.router.add_post(config["service"]["route"]["pingpong"], ping)
    app.router.add_post(config["service"]["route"]["on_dialout"], handle_on_dialout)
    app.router.add_post(config["service"]["route"]["on_ring"], handle_on_ring)
    app.router.add_post(config["service"]["route"]["on_answer"], handle_on_answer)
    app.router.add_post(config["service"]["route"]["on_hangup"], handle_on_hangup)
    app.router.add_post(config["service"]["route"]["on_pcm"], handle_on_pcm)

    tmp = config["service"]["addr"].split(":")
    if len(tmp) != 2:
        os.exit(-1)
    host = tmp[0]
    port = int(tmp[1])

    main_logger.info("server start")
    main_logger.info(config["service"]["auth_token"])
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    main()
