import json
import argparse
from types import SimpleNamespace


def parse_args(config_path):
    with open(config_path, "r") as f:
        cfg = json.loads(f.read(), object_hook=lambda d: SimpleNamespace(**d))
    return cfg