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
        user = UserInfo(username=request.POST['username'], password=request.POST['password'])
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
    try:
        user = UserInfo.objects.get(username=request.POST['username'], password=request.POST['password'])
    except UserInfo.DoesNotExist:
        return render(request, 'login.html', {'loginstatus': 'Unsuccessful login. Try Again'})
    return render(request, 'userprofile.html', {'username': user.username})
