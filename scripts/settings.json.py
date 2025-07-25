import json
import os
import sys
from typing import Any


def parse_comandline_arguments() -> None:
    commandline_args: list[str] = sys.argv


def open_vscode_settings_dot_json(path: os.PathLike[str]) -> str:
    """ """

    try:
        with open(file=path, mode="r", encoding=r"ascii") as fptr:
            vscode_settings = fptr.read()
        return vscode_settings
    except FileNotFoundError as fnf_error:
        raise RuntimeError(f"Could not find the specified settings.json file at {path}") from fnf_error


def parse_settings(settings: str) -> dict[str, Any]:
    """ """

    try:
        parsed_settings = json.loads(settings)
        return parsed_settings
    except json.decoder.JSONDecodeError as jsn_dcd_error:
        raise RuntimeError("") from jsn_dcd_error


def sort_settings(settings: dict[str, Any]) -> dict[str, Any]:
    """ """

    sorted_settings: dict[str, Any] = dict()
    for key in sorted(settings):
        if not isinstance(settings.get(key), dict):
            sorted_settings[key] = settings.get(key)
        else:
            sorted_settings[key] = {k: settings.get(key).get(k) for k in sorted(settings.get(key))}
    return sorted_settings
