"""Cancel an active schedule. Since this is the last active schedule, it
should cleanly stop the scheduler.
"""
from antevents.base import *
from utils import make_test_sensor

import asyncio

class CallAfter(DefaultSubscriber):
    def __init__(self, num_events, fn):
        self.events_left = num_events
        self.fn = fn

    def on_next(self, x):
        self.events_left -= 1
        if self.events_left == 0:
            print("calling fn %s" % self.fn)
            self.fn()

sensor = make_test_sensor(1)
sensor.subscribe(print)
s = Scheduler(asyncio.get_event_loop())
cancel_schedule = s.schedule_periodic(sensor, 1)
sensor.subscribe(CallAfter(4, cancel_schedule))
sensor.print_downstream()
s.run_forever()
print("got to end")