from django_cron import CronJobBase, Schedule
from django.utils import timezone
from datetime import timedelta, datetime

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from .models import Ip, UserIpMap, UserProfile
import requests

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
                    UserIpMap_object = UserIpMap.objects.filter(client=user)
                    for userIpMap in UserIpMap_object:
                        if len(UserIpMap.objects.filter(ip__name=userIpMap.ip.name, client__userprofile__alive=True)) == 0:
                            # No alive user is requesting that IP
                            print "Setting alive to False for IP: " + userIpMap.ip.name
                            userIpMap.ip.alive = False
                            userIpMap.ip.save()
                        else:
                            userIpMap.ip.update_min_poll_time()

class FetchIpStatus(CronJobBase):
        RUN_EVERY_MINS = 1;

        schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
        code = 'dashboard:fetch_ip_stataus'

        def do(self):
            print "Fetching Ip status"
            Ip_object_list = Ip.objects.filter(alive = 1)
            PORT = "8085"
            TIMOEOUT = 2    # 2 seconds
            for Ip_object in Ip_object_list:
                if (Ip_object.last_fetched + timedelta(minutes=Ip_object.min_poll_time)) < timezone.now():
                    url = "http://" + Ip_object.name + ":" + PORT + "/Snh_ItfReq"
                    try:
                        response = requests.head(url, timeout=TIMOEOUT)
                        Ip_object.status = response.status_code
                    except requests.Timeout:
                        Ip_object.status = "Down"
                    except requests.ConnectionError:
                        Ip_object.status = "Down"
                    Ip_object.last_fetched = timezone.now()
                    Ip_object.save()
                    print "Status set for : " + Ip_object.name 
                else:
                    print "Ignoring IP : " + Ip_object.name