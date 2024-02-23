#!/usr/bin/python3
# -*- coding: utf-8 -*-


on_pcm_schema = {
    "type": "object",
    "required": ["callID", "seq", "pcmInBase64"],
    "properties": {
        "callID": {
            "type": "string"
        },
        "seq": {
            "type": "integer"
        },
        "pcmInBase64": {
            "type": "string"
        },
        "ext": {
            "type": "string"
        },
    }
}


if __name__ == "__main__":
    pass
