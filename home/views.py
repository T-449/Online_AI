from django.shortcuts import render
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../Online_AI.settings')
django.setup()

from home.models import UserInfo


# Create your views here.

def login(request):
    return render(request, 'users/login.html', {'loginstatus': ''})


def createuser(request):
    return render(request, 'createuser.html')


def showprofile(request):
    id = request.POST['username']
    pwd = request.POST['password']
    try:
        user = UserInfo.objects.get(username=id, password=pwd)
    except UserInfo.DoesNotExist:
        try:
            user = UserInfo.objects.get(email=id, password=pwd)
        except UserInfo.DoesNotExist:
            return render(request, 'users/login.html',
                          {'loginstatus': 'Unsuccessful login. Please try Again', 'color': 'red'})
    return render(request, 'userprofile.html', {'username': user.firstname + " " + user.lastname})


def usercreation(request):
    user = UserInfo(firstname=request.POST['firstname'], lastname=request.POST['lastname'], email=request.POST['email'],
                    password=request.POST['password'], country=request.POST['country'], username=request.POST['username'])
    user.save()
    return render(request, 'users/login.html', {'loginstatus': 'User created successfully', 'color': 'green'})
