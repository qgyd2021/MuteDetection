#!/usr/bin/python3
# -*- coding: utf-8 -*-


on_dialout_schema = {
    "type": "object",
    "required": ["callID", "ts", "params", "callbackList"],
    "properties": {
        "callID": {
            "type": "string"
        },
        "ts": {
            "type": "integer"
        },
        "params": {
            "type": "string"
        },
        "callbackList": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["callbackType", "callbackUrl"],
                "properties": {
                    "callbackType": {
                        "type": "string",
                    },
                    "callbackUrl": {
                        "type": "string",
                    },
                }
            }
        },
        "ext": {
            "type": "string"
        },
    }
}


if __name__ == "__main__":
    pass
