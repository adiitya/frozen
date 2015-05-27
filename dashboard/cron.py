from django_cron import CronJobBase, Schedule
from datetime import datetime

class TestCronJob(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dashboard.test_cron_job'

    def do(self):
        print "Test cron running"
