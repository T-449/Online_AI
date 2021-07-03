from django.http import HttpResponseRedirect


def redirectToCurrent(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))