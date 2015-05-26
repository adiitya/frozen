from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import IPs, UserIpMap
from django.contrib.auth import authenticate, login, logout
from django.db.models import Min
from django.utils import timezone

# Create your views here.

def user_login(request):
    if request.user.is_authenticated():
        return HttpResponse("You are already logged in")
    error = ""
    if request.method == 'POST':
        username = request.POST['username'];
        password = request.POST['password'];
        user = authenticate(username=username, password=password);
        if user is not None:
            if user.is_active:
                login(request, user)
                #return HttpResponseRedirect(reverse('dashboard:index'))
                return HttpResponse('Successfully logged in')
            else:
                return HttpResponse('Sorry, this account is disabled')
        else:
            error = "Invalid credentials"
    return render(request, 'dashboard/login.html', { 'error': error})

def user_settings(request):
    # Checking if user is logged in or not
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:login'))

    error = "";
    if request.method == 'POST':
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            error = 'Passwords do not match'
        else:
            request.user.set_password(password1)
            request.user.save()
            return HttpResponse('Password Successfully changed')
    return render(request, 'dashboard/settings.html', { 'error': error})

def user_logout(request):
    logout(request)

    return HttpResponse('Successfully logged out')

def add_ip(request):
	#Check if user is logged in or not
	if request.user.is_authenticated():
		if request.method == 'POST':
			#Fetch this IP object from central db or create one if not their
			try: 
				IPs_object, created = IPs.objects.get_or_create(ip = request.POST['ip'])
			except KeyError:
				return HttpResponse("IP filed is blank")
			#Create an entry in client table
			try KeyError:
				UserIpMap_object = UserIpMap(request.user.id, IPs_object.id, request.POST['ip'], request.POST['polling_time'])	
			except:
				return HttpResponse("Please provide all the fields.")
			#Get minimum polling time for this IP address from global Map table
	    	min_polling_time = UserIpMap.objects.filter(ip = request.POST['ip']).aggregate(Min('polling_time'))['polling_time__min']
	    	#Update global IP table with it.
	    	IPs_object.min_poll_time = min_polling_time
	    	IPs_object.save()

	else:
		return HttpResponse("You need to log in first")

