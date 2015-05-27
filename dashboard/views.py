from django.views import generic
from django.core.urlresolvers import reverse
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import IPs, UserIpMap, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.utils import timezone
from datetime import datetime

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard/index.html')
    else:
        return HttpResponseRedirect(reverse('dashboard:login'))


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard:home'))
    error = ""
    if request.method == 'POST':
        username = request.POST['username'];
        password = request.POST['password'];
        user = authenticate(username=username, password=password);
        if user is not None:
            if user.is_active:
                login(request, user)
                set_access(request)
                #return HttpResponseRedirect(reverse('dashboard:index'))
                return HttpResponseRedirect(reverse('dashboard:home'))
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
                return HttpResponse("IP field is blank")
            #Create an entry in client table
            try:
                UserIpMap_object = UserIpMap.objects.get_or_create(client=request.user, ip=IPs_object, 
                                        defaults = {'polling_time': request.POST['polling_time']})
            except KeyError:
                return HttpResponse("Please provide all the fields.")
            IPs_object.update_min_poll_time()
            return HttpResponse("Added IP")
        else:
            return HttpResponse("Request Metod Error")

    else:
        return HttpResponseRedirect(reverse('dashboard:login'))


def delete_ip(request):
    #Check if user is logged in or not
    if request.user.is_authenticated():
        if request.method == 'POST' and 'ip' in request.POST:
            #delete entry from client table.
            try:
                IPs_object = IPs.objects.get(ip = request.POST['ip'])
            except:
                return HttpResponse("No Ip exist in main server table")
            try:
                UserIpMap.objects.filter(client = request.user, ip = IPs_object ).delete()
            except:
                return HttpResponse("No Ip exist in UserIpMap table")
            #If no other user has requested for this IP then delete it from main table as well
            if not UserIpMap.objects.filter(ip = IPs_object).exists():
                IPs.objects.filter(ip = IPs_object.ip).delete()
            #LATER redirect to home and also validate IPs
            return HttpResponse("IP deleted")

    else:
        return HttpResponse("You need to log in first")

def set_access(request):
    #Check if user is logged in or not
    if request.user.is_authenticated():
        UserProfile_object = request.user.userprofile
        #If user is dead
        if not UserProfile_object.alive: 
            UserProfile_object.alive = True
        UserProfile_object.last_access = datetime.now()
        UserProfile_object.save()
        return HttpResponse("Data for user updated")
    else:
        return HttpResponse("User id not logged in")

