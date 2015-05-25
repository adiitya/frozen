from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def login(request):
    if request.user.is_authenticated():
        return HttpResponse("You are already logged in")
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
    return render(request, 'polls/login.html', { 'error': error})

def logout(request):
    logout(request)

    return HttpResponse('Successfully logged out')
