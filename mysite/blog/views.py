from django.shortcuts import render
from .models import Post
from django.views import generic
from django.db.models import Q

# Create your views here.
# def posts(request):
#     return render(request,
#                   template_name="posts.html",
#                   context={'posts': Post.objects.all()})


# def post(request, pk):
#     return render(request,
#                   template_name="post.html",
#                   context={'post': Post.objects.get(pk=pk)})

class PostListView(generic.ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 2


class PostDetailView(generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"


def search(request):
    query = request.GET.get("query")
    context = {
        'query': query,
        'posts': Post.objects.filter(Q(title__icontains=query) |
                                     Q(content__icontains=query) |
                                     Q(author__username__icontains=query)),
    }
    return render(request, template_name="search.html", context=context)

