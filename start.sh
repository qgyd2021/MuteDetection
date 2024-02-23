#!/usr/bin/env bash

rm -rf nohup.out
rm -rf logs/
mkdir -p logs/

nohup python3 run_mute_detection_server.py > nohup.out &
