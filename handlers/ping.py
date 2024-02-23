#!/bin/python3
# coding=utf-8
import jsonschema

from route_wrap.ping_route_wrap import ping_route_wrap
from schema.ping_schema import ping_schema
from exception import ExpectedError


# 请求体
req_body = {
    "ping_ms": 0,  # 调用方时间戳（毫秒级）
    "ping_msg": "str",  # 调用方消息
    "ext": "str",  # 调用方的透传字段
}

# 响应体
rsp_body = {
    "retCode": 0,  # 返回码，0:成功，其他:失败
    "retMsg": "str",  # 返回说明，对应retCode的一个解析
    "responseID": "str",  # 随机唯一id，用于请求追踪，定位问题时需要提供该次请求的responseID
    "ext": "str",  # 调用方的透传字段
}


@ping_route_wrap
async def ping(request):
    js = await request.json()

    try:
        jsonschema.validate(js, ping_schema)
    except (jsonschema.exceptions.ValidationError,
            jsonschema.exceptions.SchemaError,) as e:
        raise ExpectedError(
            status_code=60401,
            message="request body invalid.",
            detail=str(e)
        )

    ext = js.get("ext")
    return ext
