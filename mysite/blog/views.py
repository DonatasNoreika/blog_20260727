from django.shortcuts import render
from .models import Post

# Create your views here.
def posts(request):
    return render(request,
                  template_name="posts.html",
                  context={'posts': Post.objects.all()})


def post(request, pk):
    return render(request,
                  template_name="post.html",
                  context={'post': Post.objects.get(pk=pk)})