from django_cron import CronJobBase, Schedule
from django.utils import timezone
from datetime import timedelta

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .models import Ip, UserIpMap, UserProfile

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
        print "Running SetMinPollTimeCronJob"
        # Iterating over every IP in Ip
        for IP in Ip.objects.all():
            IP.update_min_poll_time();
            print "Updating min_poll_time for " + IP.name

class CleanInactiveUsers(CronJobBase):
    RUN_EVERY_MINS = 1

    # In hours
    USER_TIMEOUT = 10

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'dashboard.clean_inactive_users'

    def do(self):
        print "CleanInactiveUsers"
        # Iterating over all userse
        for user in User.objects.all():
            if user.userprofile.alive:
                print "Checking alive user: " + user.username
                if (user.userprofile.last_access + timedelta(hours=self.USER_TIMEOUT)) < timezone.now():
                    print "Removing user: " + user.username
                    # Removing user
                    user.userprofile.alive = False
                    user.userprofile.save()

                    # Logging out user
                    [s.delete() for s in Session.objects.all() if s.get_decoded().get('_auth_user_id') == str(user.id)]

                    # Setting IP's alive to False in Ip table if it's the only client using it
                    for userIpMap in UserIpMap.objects.filter(client=user):
                        if len(UserIpMap.objects.filter(ip__name=userIpMap.ip.name, client__userprofile__alive=True)) == 0:
                            # No alive user is requesting that IP
                            print "Setting alive to False for IP: " + userIpMap.ip.name
                            userIpMap.ip.alive = False
                            userIpMap.ip.save()
                        else:
                            userIpMap.ip.update_min_poll_time()
