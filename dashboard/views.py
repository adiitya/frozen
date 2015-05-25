from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import IPs, UserIpMap
from django.contrib.auth import authenticate, login, logout
from django.db.models import Min
from django.utils import timezone

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