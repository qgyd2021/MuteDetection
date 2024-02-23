#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json

import jsonschema

from exception import ExpectedError
from route_wrap.voice_event_route_wrap import voice_event_route_wrap
from schema.on_dialout_schema import on_dialout_schema
from service.mute_detection import manager


@voice_event_route_wrap
async def handle_on_dialout(request):
    js = await request.json()

    try:
        jsonschema.validate(js, on_dialout_schema)
    except (jsonschema.exceptions.ValidationError,
            jsonschema.exceptions.SchemaError,) as e:
        raise ExpectedError(
            status_code=60401,
            message="request body invalid.",
            detail=str(e)
        )

    call_id = js["callID"]
    ts = js["ts"]
    callback_list = js["callbackList"]
    ext = js.get("ext")

    params = js["params"]
    params = json.loads(params)

    scene_id = params["scene_id"]
    language = params["language"]

    stop_flag = await manager.on_dialout(
        call_id=call_id,
        ts=ts,
        callback_list=callback_list,
        scene_id=scene_id,
        language=language,
    )
    return stop_flag, ext
