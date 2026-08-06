from django.shortcuts import render
from .models import Post

# Create your views here.
def posts(request):
    return render(request,
                  template_name="posts.html",
                  context={'posts': Post.objects.all()})