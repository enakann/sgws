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
from storage_grid.libs.sizer import Sizer
import logging
import json
import ast

logger=logging.getLogger("kannan")


class SGWSForwardSizing(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('inputs',
                        type=str,
                        required=True,
                        help="This field cannot be blank")

    def get(self):
        default_input={
        "applianceModelFull":"SG6060 (58x10TB FIPS)",
        "storageNeededInTb":5000,
        "avgObjectSize":4,
        "smallObjectIngestRateObjps":1800,
        "largeObjectIngestThrouhputInMbps":900,
        "hwLevelDataProtection":"DDP8",
        "iLMRuleApplied":"2-site: 2 replicas"
    }
        sizer=Sizer(default_input)
        ret=sizer.size()
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