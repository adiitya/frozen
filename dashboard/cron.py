from django_cron import CronJobBase, Schedule
from datetime import datetime

from .models import IPs, UserIpMap

class TestCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dashboard.test_cron_job'

    def do(self):
        print "Test cron running " + datetime.now()

class SetMinPollTimeCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dashboard.set_min_poll_time_cron_job'

    def do(self):
        # Iterating over every IP in IPs
        for IP in IPs.objects.all():
            



