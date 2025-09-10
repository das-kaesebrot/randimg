import os
from typing import Union


class SvgIcons:
    _icon_map: dict[str, str]

    def __init__(self, directory: str = "resources/svg"):
        self._icon_map = {}

        for filename in os.listdir(directory):
            if filename.lower().endswith(".svg"):
                with open(filename, "r") as f:
                    icon_name = os.path.splitext(os.path.basename(filename))[0]
                    self._icon_map[icon_name] = f.read()

    def get(self, icon_name: str) -> Union[str, None]:
        return self._icon_map.get(icon_name)
