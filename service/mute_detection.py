#!/usr/bin/python3
# -*- coding: utf-8 -*-
import base64
import logging
from pathlib import Path
import re
import tempfile
from typing import Dict, List
import zipfile

import numpy as np

import settings
from settings import project_path
from exception import ExpectedError

api_logger = logging.getLogger("api")
main_logger = logging.getLogger("main")


class MuteDetectionProcessContext(object):
    def __init__(self,
                 call_id: str, scene_id: str, language: str,
                 callback_list: List[dict]
                 ):
        self.call_id = call_id
        self.scene_id = scene_id
        self.language = language
        self.callback_list = callback_list

        self.sample_rate = 8000
        self.forward_duration_s = 2
        self.min_inputs_length = self.forward_duration_s * self.sample_rate

        config = settings.get_config()
        language_to_thresholds: dict = config["settings"]["language_to_thresholds"]
        thresholds = language_to_thresholds.get(self.scene_id)
        if thresholds is None:
            thresholds = language_to_thresholds.get(self.language)
        if thresholds is None:
            raise AssertionError("language and scene_id invalid.")

        self.thresholds = thresholds

        self.on_dialout_ts = -1
        self.on_ring_ts = -1
        self.on_answer_ts = -1
        self.on_hangup_ts = -1

        # context
        self.signal_cache: np.ndarray = np.zeros(shape=(0,), dtype=np.int16)

        self.energy = 0.0
        self.duration = 0.0

        self.message = ""
        self.stop_flag: int = 0

    def process_callback_list(self, label: str = "voicemail"):
        msg = """
        report mute_detect;
        call_id: {};
        duration: {};
        message: {};
        """.format(self.call_id,
                   self.duration,
                   self.message,
                   )
        msg = re.sub(r"[\u0020]{4,}", "", msg)
        main_logger.info(msg)

    def add_on_dialout_ts(self, ts: int) -> int:
        msg = "on_dialout, call_id: {}; ts: {}".format(self.call_id, ts)
        main_logger.info(msg)
        self.on_dialout_ts = ts
        return ts

    def add_on_ring_ts(self, ts: int) -> int:
        msg = "on_ring, call_id: {}; ts: {}".format(self.call_id, ts)
        main_logger.info(msg)
        self.on_ring_ts = ts
        return ts

    def add_on_answer_ts(self, ts: int) -> int:
        msg = "on_answer, call_id: {}; ts: {}".format(self.call_id, ts)
        main_logger.info(msg)
        self.on_answer_ts = ts
        return ts

    def add_on_hangup_ts(self, ts: int) -> int:
        msg = "on_hangup, call_id: {}; ts: {}".format(self.call_id, ts)
        main_logger.info(msg)
        self.on_hangup_ts = ts
        self.stop_flag = 1
        return ts

    def update(self, pcm_in_base64: str):
        # only save the pcm when answer.
        if self.on_answer_ts > 0:
            base64byte = pcm_in_base64.encode("utf-8")
            wav_bytes = base64.b64decode(base64byte)
            signal = np.frombuffer(wav_bytes, dtype=np.int16)
            self.signal_cache = np.concatenate([self.signal_cache, signal])

    def infer(self, inputs: np.ndarray):
        # infer
        inputs = np.array(inputs, dtype=np.float32)
        inputs = inputs / (1 << 15)
        energy = np.sum(np.square(inputs))
        return round(energy, 4)

    def decision(self) -> bool:
        flag = False
        for item in self.thresholds:
            d = item["duration"]
            t = item["threshold"]

            if self.duration >= d:
                if self.energy < t:
                    self.message = "energy: {} < threshold: {}".format(self.energy, t)
                    flag = True
                    break
        return flag

    def add_on_pcm(self, pcm_in_base64: str) -> None:
        if self.stop_flag == 1:
            return None
        self.update(pcm_in_base64)
        if len(self.signal_cache) < self.min_inputs_length:
            return None

        l = len(self.signal_cache)
        rest = l % self.min_inputs_length

        for span_i in range(0, l-rest, self.min_inputs_length):
            self.duration += self.forward_duration_s

            inputs = self.signal_cache[:span_i + self.min_inputs_length]
            self.energy = self.infer(inputs)
            decision_flag = self.decision()

            if decision_flag:
                self.process_callback_list(label="mute_detect")
                self.stop_flag = 1

            if self.duration >= self.thresholds[-1]["duration"]:
                self.stop_flag = 1

        self.signal_cache = self.signal_cache[-rest:] if rest != 0 else np.zeros(shape=(0,), dtype=np.int16)
        return None


class MuteDetectionManager(object):
    def __init__(self):
        self.call_id_to_context: Dict[str, MuteDetectionProcessContext] = dict()

    async def on_dialout(self,
                         call_id: str, ts: int,
                         callback_list: List[dict],
                         scene_id: str, language: str,
                         ) -> int:
        # create context
        context = MuteDetectionProcessContext(
            call_id=call_id, scene_id=scene_id, language=language,
            callback_list=callback_list
        )
        context.add_on_dialout_ts(ts)
        self.call_id_to_context[call_id] = context

        return context.stop_flag

    async def on_ring(self,
                      call_id: str, ts: int,
                      ):
        context = self.call_id_to_context.get(call_id)
        if context is None:
            raise ExpectedError(
                status_code=1,
                message="context not found.",
            )

        context.add_on_ring_ts(ts)
        return context.stop_flag

    async def on_answer(self,
                        call_id: str, ts: int,
                        ):
        context = self.call_id_to_context.get(call_id)
        if context is None:
            raise ExpectedError(
                status_code=1,
                message="context not found.",
            )

        context.add_on_answer_ts(ts)
        return context.stop_flag

    async def on_hangup(self,
                        call_id: str, ts: int,
                        ):
        context = self.call_id_to_context.get(call_id)
        if context is None:
            raise ExpectedError(
                status_code=1,
                message="context not found.",
            )
        context.add_on_hangup_ts(ts)
        return context.stop_flag

    async def on_pcm(self,
                     call_id: str,
                     pcm_in_base64: str,
                     ):

        context = self.call_id_to_context.get(call_id)
        if context is None:
            raise ExpectedError(
                status_code=1,
                message="context not found.",
            )

        context.add_on_pcm(pcm_in_base64)
        return context.stop_flag


manager = MuteDetectionManager()


def main():
    return


if __name__ == '__main__':
    main()
