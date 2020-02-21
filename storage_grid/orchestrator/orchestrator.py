"""
Copyright (c) 1992-2020 NetApp, Inc.
All rights reserved.
"""

__author__ = "Naveen Jadar"

from cvo_sizer.orchestrator.properties import Properties
from cvo_sizer.resources.aws_sizing import AwsForwardSizing


class Orchestrator:
    def __init__(self, wflow):
        self.wflow = wflow

    def do_aws_sizing(self, awsForwardInput):
        prop = Properties(self.wflow)
        fwd_sizing = AwsForwardSizing()
        results = fwd_sizing.getAwsForwardSizingResult(awsForwardInput)
        return results
