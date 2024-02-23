#!/usr/bin/env bash

kill -9 `ps -aef | grep 'run_mute_detection_server.py' | grep -v grep | awk '{print $2}'`
