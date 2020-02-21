"""
Copyright (c) 1992-2020 NetApp, Inc.
All rights reserved.
"""

__author__ = "Naveen Jadar"

import cvo_sizer.common.templates as templates
import json


class Properties:
    def __init__(self, wflow):
        self.wflow = wflow
        pass

    def get_input_template(self, wflow):
        template = json.loads(templates.inputTemplates[wflow])
        return template

    def get_output_template(self, wflow):
        template = json.loads(templates.outputTemplates[wflow])
        return template
