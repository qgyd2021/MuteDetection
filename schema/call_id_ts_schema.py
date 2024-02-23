#!/usr/bin/python3
# -*- coding: utf-8 -*-


call_id_ts_schema = {
    "type": "object",
    "required": ["callID", "ts"],
    "properties": {
        "callID": {
            "type": "string"
        },
        "ts": {
            "type": "integer"
        },
        "ext": {
            "type": "string"
        },
    }
}


if __name__ == "__main__":
    pass
