
"""
Copyright (c) 1992-2020 NetApp, Inc.
All rights reserved.
"""

__author__ = "Naveen Jadar"

from enum import Enum


class CloudVendor(Enum):
    aws = 'AWS'
    azure = 'AZURE'
    gcp = 'GCP'


class ThroughputUnit(Enum):
    IOPS = 'IOPS'
    MBPS = 'MBPS'


class CapacityUnit(Enum):
    TB = 'TB'
    TiB = 'TiB'

