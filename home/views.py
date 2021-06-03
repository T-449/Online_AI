from django.shortcuts import render
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '../Online_AI.settings')
django.setup()

from home.models import UserInfo


# Create your views here.

def login(request):
    f = open("usercreated.txt", "r")
    line = str(f.readline())
    print(line)
    f.close()
    if line == '1':
        user = UserInfo(firstname=request.POST['firstname'], lastname=request.POST['lastname'], email=request.POST['email'], password=request.POST['password'],
                        country=request.POST['country'], username=request.POST['username'])
        user.save()
        f = open("usercreated.txt", "w")
        f.write("0")
        f.close()
    return render(request, 'login.html', {'loginstatus': ''})


def createuser(request):
    f = open("usercreated.txt", "w")
    f.write("1")
    f.close()
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
            return render(request, 'login.html', {'loginstatus': 'Unsuccessful login. Please try Again'})
    return render(request, 'userprofile.html', {'username': user.firstname + " " + user.lastname})
