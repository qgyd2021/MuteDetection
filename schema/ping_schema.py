#!/usr/bin/python3
# -*- coding: utf-8 -*-


ping_schema = {
    "type": "object",
    "required": ["ping_ms", "ping_msg"],
    "properties": {
        "ping_ms": {
            "type": "integer"
        },
        "ping_msg": {
            "type": "string"
        },
        "ext": {
            "type": "string"
        },
    }
}


if __name__ == "__main__":
    pass
