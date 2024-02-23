#!/usr/bin/python3
# -*- coding: utf-8 -*-
import jsonschema

from exception import ExpectedError
from route_wrap.voice_event_route_wrap import voice_event_route_wrap
from schema.call_id_ts_schema import call_id_ts_schema
from service.mute_detection import manager


@voice_event_route_wrap
async def handle_on_answer(request):
    js = await request.json()

    try:
        jsonschema.validate(js, call_id_ts_schema)
    except (jsonschema.exceptions.ValidationError,
            jsonschema.exceptions.SchemaError,) as e:
        raise ExpectedError(
            status_code=60401,
            message="request body invalid.",
            detail=str(e)
        )

    call_id = js["callID"]
    ts = js["ts"]
    ext = js.get("ext")

    stop_flag = await manager.on_answer(
        call_id=call_id,
        ts=ts,
    )
    return stop_flag, ext
