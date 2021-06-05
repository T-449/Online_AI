from django.shortcuts import render
from .models import Post

# Create your views here.
def test(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'Test/test.html', context)
