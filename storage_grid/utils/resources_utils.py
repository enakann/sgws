
"""
Copyright (c) 1992-2018 NetApp, Inc.
All rights reserved.
"""

__author__ = "Padmanabham Nooka"

from flask_restful import reqparse
import ast
from src.common.exceptions import SizingError
from src.common.error_msg import ErrorMessage
import json

class SizingDetails:
    def __init__(self):
        pass

    def get_sizing_input(self):
        """Deserialize the JSON object and returns the input"""
        parser = reqparse.RequestParser()
        parser.add_argument('inputs', type=str, required=True)
        args = parser.parse_args()
        sizingInput = json.loads(args['inputs'])
        return sizingInput

    def set_sizing_status(self, sizing_output, e=None):
        """Updating the sizing status"""
        sizingStatus = {}
        if e:
            if isinstance(e, SizingError):
                sizingStatus = {
                    'statusCode': e.error_code,
                    'statusString': e.error_string
                }
            else:
                sizingStatus = {
                    'statusCode': ErrorMessage.ERR_CSI_FAILED.name,
                    'statusString': ErrorMessage.ERR_CSI_FAILED.value
                }
        else:
            sizingStatus = {
                'statusCode': ErrorMessage.SUCCESS.name,
                'statusString': ErrorMessage.SUCCESS.value
            }

        sizing_output['sizingStatus'] = sizingStatus
        return

