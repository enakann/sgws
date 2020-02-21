
"""
Copyright (c) 1992-2020 NetApp, Inc.
All rights reserved.
"""

__author__ = "Naveen Jadar"


class SizingError(Exception):
    def __init__(self, error, **kwargs):
        self.error_code = error.name
        self.error_string = error.value.format(**kwargs)
