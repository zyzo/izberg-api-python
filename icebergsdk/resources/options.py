# -*- coding: utf-8 -*-

from icebergsdk.resources.base import UpdateableIcebergObject

class Option(UpdateableIcebergObject):
    endpoint = 'option'

class OptionAnswer(UpdateableIcebergObject):
    endpoint = 'option_answer'
