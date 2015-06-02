from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from dashboard.models import Ip, UserIpMap, UserProfile
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
import re
from dashboard import views


class ValidateRequestMiddleware:

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            if request.META['PATH_INFO'] == '/login/' or 'admin' in request.META['PATH_INFO'] :
                None
            else:
                return HttpResponseRedirect(reverse('dashboard:login'))
        else:
            None