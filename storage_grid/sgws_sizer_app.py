"""
Copyright (c) 1992-2020 NetApp, Inc.
All rights reserved.
"""

""" Entry point into the application """

__author__ = "Naveen Jadar"

import os
import sys
from flask import Flask
from flask_restful import Api
from storage_grid.resources.forward_sizing import SGWSForwardSizing
from storage_grid.utils.logger import Logger

loggerObj=Logger("kannan")
logger=loggerObj.get_logger()


logger.info("test1")
app = Flask(__name__)
api = Api(app)



def main(restPort):
    api.add_resource(SGWSForwardSizing, '/sgws/sg/forward')
    app.run(host='0.0.0.0', port=restPort, debug=os.environ.get('DEBUG', 0))


if __name__ == '__main__':
    main(8000)