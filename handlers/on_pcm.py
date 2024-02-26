#!/usr/bin/python3
# -*- coding: utf-8 -*-
import base64

import numpy as np
import jsonschema

from exception import ExpectedError
from route_wrap.voice_event_route_wrap import voice_event_route_wrap
from schema.on_pcm_schema import on_pcm_schema
from service.mute_detection import manager


# 请求体
req_body = {
    'callID': 'str',  # 通话id
    'seq': 0,  # 媒体包的序号，[0,MAX_INT]
    'pcmInBase64': 'str',  # 数据-base64编码
}

# 响应体
rsp_body = {
    'code': 0,  # 返回码，0:成功，其他:失败
    'message': 'str',  # 返回说明，对应retCode的一个解析
    'responseID': 'str',  # 随机唯一id，用于请求追踪，定位问题时需要提供该次请求的responseID
    'stopFlag': 0,  # 停送音频标识,0:none,1:停止送量
}


@voice_event_route_wrap
async def handle_on_pcm(request):
    js = await request.json()

    try:
        jsonschema.validate(js, on_pcm_schema)
    except (jsonschema.exceptions.ValidationError,
            jsonschema.exceptions.SchemaError,) as e:
        raise ExpectedError(
            status_code=60401,
            message="request body invalid.",
            detail=str(e)
        )

    call_id = js["callID"]
    seq = js["seq"]
    pcm_in_base64 = js["pcmInBase64"]
    ext = js.get("ext")

    stop_flag = await manager.on_pcm(
        call_id=call_id,
        pcm_in_base64=pcm_in_base64,
    )
    return stop_flag, ext
