#!/usr/bin/python3
# -*- coding: utf-8 -*-
import asyncio
import os
from pathlib import Path

import yaml


project_path = os.path.abspath(os.path.dirname(__file__))
project_path = Path(project_path)

log_directory = os.path.join(project_path, "logs")
os.makedirs(log_directory, exist_ok=True)


app_yaml_file = project_path / "conf/app.yaml"


# app yaml config
config = None


def get_config():
    global config

    with open(app_yaml_file.as_posix(), encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config


if __name__ == '__main__':
    pass
