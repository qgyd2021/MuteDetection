#!/usr/bin/python3
# -*- coding: utf-8 -*-
import copy
import json


def json_2_str(d):
    max_list_length = 20
    max_dict_length = 10
    max_str_length = 50

    if isinstance(d, list):
        d = [json_2_str(e) for e in d[:max_list_length]]
    elif isinstance(d, dict):
        d = {k: json_2_str(v) for k, v in list(d.items())[:max_dict_length]}
    elif isinstance(d, str) and len(d) > max_str_length:
        d = "[type: {}, len: {}, abstract: {}]".format(
            type(d), len(d), d[:max_str_length]
        )
    else:
        d = d

    return d


if __name__ == '__main__':
    pass
