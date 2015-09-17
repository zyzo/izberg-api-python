# -*- coding: utf-8 -*-
from icebergsdk.resources.base import UpdateableIcebergObject


class AvailabilityCalendar(UpdateableIcebergObject):
    endpoint = 'availability_calendar'


class AvailabilityTimeSlot(UpdateableIcebergObject):
    endpoint = 'availability_timeslot'
