import os
import json


class JSON:
    def __init__(self, filename):
        self._file = filename

    def is_valid_json(self):
        """validates if json is valid"""
        try:
            json_object = json.loads(self._file)
        except (ValueError, TypeError) as e:
            raise
