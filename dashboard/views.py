from django.views import generic
from django.core.urlresolvers import reverse
from django.core import serializers
from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from .models import Ip, UserIpMap, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext, loader
from django.utils import timezone
from datetime import datetime
import json, time

# Create your views here.

def index(request):
    UserIpMaps = UserIpMap.objects.filter(client = request.user)
    IPs = []
    for userIpMap in UserIpMaps:
        IPs.append(userIpMap.ip)
    return render(request, 'dashboard/index.html', {'IPs' : IPs, 'user' : request.user})


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
                #return HttpResponseRedirect(reverse('dashboard:index'))
                return HttpResponseRedirect(reverse('dashboard:home'))
            else:
                return HttpResponse('Sorry, this account is disabled')
        else:
            error = "Invalid credentials"
    return render(request, 'dashboard/login.html', { 'error': error})

def user_settings(request):
    # Checking if user is logged in or not
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

    return HttpResponseRedirect(reverse('dashboard:login'))

def ip_status(request):
    ip_address = request.GET['ip']
    try:
        Ip_object =Ip.objects.get(name=ip_address)
        if not Ip_object.alive:
            return JsonResponse({'error': 'IP entry is dead'})
        response_data = {}
        response_data['name'] = Ip_object.name
        response_data['status'] = Ip_object.status
        response_data['last_fetched'] = Ip_object.last_fetched.strftime("%b %d, %Y, %I:%M %P")
        response_data['min_poll_time'] = Ip_object.min_poll_time
        return JsonResponse(response_data)
    except:
        return JsonResponse({'error': 'IP does not exist'})

def add_ip(request):
    if request.method == 'GET':
        #Fetch this IP object from central db or create one if not their    
        try: 
            Ip_object, created = Ip.objects.get_or_create(name = request.GET['ip'])
        except KeyError:
            return JsonResponse({'error': 'IP field is blank'})
        #Create an entry in client table
        try:
            UserIpMap_object,created = UserIpMap.objects.get_or_create(client=request.user, ip=Ip_object, 
                                    defaults = {'polling_time': request.GET['polling_time']})
            #If same IP existed before then this Ip is not created as new
            if not created:
                #Update polling time
                UserIpMap_object.polling_time = request.GET['polling_time']
                UserIpMap_object.save()
        except KeyError:
            return JsonResponse({'error': 'Please provide all the fields.'})
        Ip_object.update_min_poll_time()
        if created :
            return JsonResponse({'success': 'IP Added'})
        else :
            return JsonResponse({'success': 'IP already exist','duplicate':'true'})
    else:
        return JsonResponse({'error': 'Request Metod Error'})


def delete_ip(request):
    if request.method == 'GET' and 'ip' in request.GET:
        #delete entry from client table.
        try:
            Ip_object = Ip.objects.get(name = request.GET['ip'])
        except:
            return JsonResponse({"error": "No Ip exist in main server table"})
        try:
            UserIpMap.objects.filter(client = request.user, ip = Ip_object ).delete()
        except:
            return JsonResponse({"error": "No Ip exist in UserIpMap table"})
        #If no other user has requested for this IP then delete it from main table as well
        if not UserIpMap.objects.filter(ip = Ip_object).exists():
            Ip.objects.filter(name = Ip_object.name).delete()
        #LATER redirect to home and also validate Ip
        return JsonResponse({"success": "IP deleted"})

def set_access(request):
    #Check if user is logged in or not
    if request.user.is_authenticated():
        UserProfile_object = request.user.userprofile
        UserProfile_object.last_access = datetime.now()
        UserProfile_object.save()
        return HttpResponse("Data for user updated")
    else:
        return HttpResponse("User id not logged in")

def check_dead_make_ip_alive(request):
    UserProfile_object = request.user.userprofile
    #If user is dead
    if not UserProfile_object.alive: 
        UserProfile_object.alive = True
        UserProfile_object.save()
        #Fecth all the UserIpMap 
        UserIpMap_object_list = UserIpMap.objects.filter(client =request.user)
        for UserIpMap_object in UserIpMap_object_list:
            Ip_object = Ip.objects.get(name = UserIpMap_object.ip.name)
            Ip_object.alive = True
            Ip_object.save()
            Ip_object.update_min_poll_time()
    return HttpResponse("Done")

def get_ip_by_user(request):
    if request.user.is_authenticated():
        Ip_list = UserIpMap.objects.filter(client = request.user)
        ip_json = {}
        for count, Ip_list_object in enumerate(Ip_list):
            data = { "address" : Ip_list_object.ip.name,
                     "last_fetched" : int(time.mktime(Ip_list_object.ip.last_fetched.timetuple())*1000),
                     "min_poll_time" : Ip_list_object.ip.min_poll_time,
                     "status" : Ip_list_object.ip.status
                    }
            ip_json[count] = data
        return JsonResponse(ip_json)
    else:
        return JsonResponse("Login Required")