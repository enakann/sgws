
"""
Copyright (c) 1992-2020 NetApp, Inc.
All rights reserved.
"""

__author__ = "Naveen Jadar"

fwdOutput = '''fwd output template'''

fwdInput = '''{"sizingTitle":"Workload 1","sizingType":"FORWARD"}'''

inputTemplates = dict.fromkeys(('aws', 'azure', 'gcp'), fwdInput)

outputTemplates = dict.fromkeys(('aws', 'azure', 'gcp'), fwdOutput)
