#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import base64
import hashlib
import json
from pathlib import Path
import os
import re
import sys
import time
import uuid
from tqdm import tqdm

pwd = os.path.abspath(os.path.dirname(__file__))
project_path = Path(os.path.join(pwd, '../'))
sys.path.append(project_path)

import numpy as np
import requests
from scipy.io import wavfile
from tqdm import tqdm


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        type=str,
    )
    parser.add_argument(
        "--port",
        default=30090,
        type=int,
    )
    args = parser.parse_args()
    return args


class VoiceProxyTest(object):

    def __init__(self,
                 host: str = "127.0.0.1",
                 port: int = 30090,
                 token: str = "12345"
                 ):
        self.host = host
        self.port = port
        self.token = token

    def post_on_dialout(self, call_id: str, scene_id: str, language: str):
        ts = int(time.time() * 1000)

        url = "http://{}:{}/voice/event/on_dailout".format(self.host, self.port)

        headers = {
            'Content-Type': 'application/json',
            "Token": self.token
        }
        params = {
            "scene_id": scene_id,
            "language": language
        }
        data = {
            "callID": call_id,
            "ts": ts,
            "params": json.dumps(params),
            "callbackList": [
                {
                    "callbackType": "callbackType",
                    "callbackUrl": "callbackUrl"
                }
            ],
            "ext": "ext"
        }
        resp = requests.request("POST", url=url, headers=headers, data=json.dumps(data))
        if resp.status_code != 200:
            print(resp)
            print(resp.text)
            return 1
        else:
            js = resp.json()
            stop_flag = js["stopFlag"]
            return stop_flag

    def post_on_ring(self, call_id: str):
        ts = int(time.time() * 1000)

        url = "http://{}:{}/voice/event/on_ring".format(self.host, self.port)

        headers = {
            "Content-Type": "application/json",
            "Token": self.token
        }
        data = {
            "callID": call_id,
            "ts": ts,
            "ext": "ext"
        }
        resp = requests.request("POST", url=url, headers=headers, data=json.dumps(data))
        if resp.status_code != 200:
            print(resp)
            print(resp.text)
            return 1
        else:
            js = resp.json()
            stop_flag = js["stopFlag"]
            return stop_flag

    def post_on_answer(self, call_id: str):
        ts = int(time.time() * 1000)

        url = "http://{}:{}/voice/event/on_answer".format(self.host, self.port)

        headers = {
            "Content-Type": "application/json",
            "Token": self.token
        }
        data = {
            "callID": call_id,
            "ts": ts,
            "ext": "ext"
        }

        resp = requests.request("POST", url=url, headers=headers, data=json.dumps(data))
        if resp.status_code != 200:
            print(resp)
            print(resp.text)
            return 1
        else:
            js = resp.json()
            stop_flag = js["stopFlag"]
            return stop_flag

    def post_on_pcm(self, call_id: str, pcm_in_base64: str):
        url = "http://{}:{}/voice/event/on_pcm".format(self.host, self.port)

        headers = {
            "Content-Type": "application/json",
            "Token": self.token
        }
        data = {
            "callID": call_id,
            "seq": 0,
            "pcmInBase64": pcm_in_base64,
            "ext": "ext"
        }

        resp = requests.request("POST", url=url, headers=headers, data=json.dumps(data))

        if resp.status_code != 200:
            print(resp)
            print(resp.text)
            return 1
        else:
            js = resp.json()
            print(js)
            stop_flag = js["stopFlag"]
            return stop_flag

    def post_on_hangup(self, call_id: str):
        ts = int(time.time() * 1000)

        url = "http://{}:{}/voice/event/on_hangup".format(self.host, self.port)

        headers = {
            "Content-Type": "application/json",
            "Token": self.token
        }
        data = {
            "callID": call_id,
            "ts": ts,
            "ext": "ext"
        }

        resp = requests.request("POST", url=url, headers=headers, data=json.dumps(data))
        if resp.status_code != 200:
            print(resp)
            print(resp.text)
            return 1
        else:
            js = resp.json()
            stop_flag = js["stopFlag"]
            return stop_flag


def main():
    args = get_args()

    proxy = VoiceProxyTest(host=args.host, port=args.port)

    filename = project_path / "data/voicemail_detection_examples/id-ID/voicemail/3300999628164852605_34240.wav"

    call_id = str(uuid.uuid4())

    sample_rate, signal = wavfile.read(filename)

    proxy.post_on_dialout(call_id=call_id, scene_id="h3f25ivhb0c0", language="id-ID")
    proxy.post_on_ring(call_id=call_id)

    # 20ms
    n_samples = int(20 / 1000 * sample_rate)
    wav_ts = 0

    for i in tqdm(range(0, len(signal), n_samples)):
        sub_signal = signal[i:i+n_samples]
        pcm_signal = sub_signal.tobytes()
        pcm_in_base64 = base64.b64encode(pcm_signal).decode("utf-8")

        stop_flag = proxy.post_on_pcm(call_id=call_id, pcm_in_base64=pcm_in_base64)

        if stop_flag == 1:
            break

        wav_ts += 20
        if wav_ts == 34240:
            proxy.post_on_answer(call_id=call_id)

    proxy.post_on_hangup(call_id=call_id)
    return


if __name__ == "__main__":
    main()
