"""
Copyright (c) 1992-2020 NetApp, Inc.
All rights reserved.
"""

"""
"""

from flask import Flask,request,jsonify
from flask_restful import Resource,reqparse
from flask_jwt_extended import (jwt_required,
                                fresh_jwt_required,
                                get_jwt_claims,
                                jwt_optional,
                                get_jwt_identity)
from libs.sizer import Sizer
import logging
import json
import ast
from flask_expects_json import expects_json
from cerberus import Validator
#v.schema = {'role': {'type': 'list', 'allowed': ['agent', 'client', 'supplier']}}
"""
>>> schema = {'prop1':
...           {'type': 'number',
...            'anyof':
...            [{'min': 0, 'max': 10}, {'min': 100, 'max': 110}]}}


"""
schema = {
            'applianceModelFull': {'type': 'string', 'required': True, 'minlength': 10},
            'storageNeededInTb': {'type': 'integer', 'required': True},
            'avgObjectSize': {'type': 'integer', 'required': True,'allowed':[4,8,10,12]},
            'smallObjectIngestRateObjps': {'type': 'integer', 'required': True, 'min': 1800,'max':2500},
            'largeObjectIngestThrouhputInMbps': {'type': 'integer', 'required': True},
            'hwLevelDataProtection': {'type': 'string', 'required': True},
            'iLMRuleApplied': {'type': 'string', 'required': True}
        }

logger=logging.getLogger("kannan")


class SGWSForwardSizing(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('inputs',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    def get(self):
        v=Validator()
        v.schema=schema
        data = self.parser.parse_args()
        data = ast.literal_eval(data["inputs"])
        print(data)
        if not v.validate(data,schema):
            return {"description":v.errors},400
        else:
            default_input = {
                "applianceModelFull": "SG6060 (58x10TB FIPS)",
                "storageNeededInTb": 5000,
                "avgObjectSize": 4,
                "smallObjectIngestRateObjps": 1800,
                "largeObjectIngestThrouhputInMbps": 900,
                "hwLevelDataProtection": "DDP8",
                "iLMRuleApplied": "2-site: 2 replicas"
            }
            sizer = Sizer(default_input)
            ret = sizer.size()
            return ret


    def post(self):
        #import pdb;pdb.set_trace()
        data = self.parser.parse_args()
        print(data)
        data=ast.literal_eval(data["inputs"])
        print(data)
        sizer=Sizer(data)
        ret=sizer.size()
        return ret
