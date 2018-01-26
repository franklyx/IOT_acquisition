#!/usr/bin/env python
# -*-coding:utf-8 -*-

"""
Customize some of the error types
"""


class FactoryMissingError(Exception):
    def __init__(self):
        self.value = "You have not registered the factory yet."


class FactoryIdMismatchError(Exception):
    def __init__(self):
        self.value = "The factoryId mismatch between config file and mongodb."


class DeviceMissingError(Exception):
    def __init__(self):
        self.value = "You have not registered the device yet."
