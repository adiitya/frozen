from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

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
