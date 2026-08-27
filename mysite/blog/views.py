from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from .models import Post, Comment, CustomUser
from django.views import generic
from django.db.models import Q
# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreateForm, CommentForm

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
    paginate_by = 5


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.pk})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.get_object()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


def search(request):
    query = request.GET.get("query")
    context = {
        'query': query,
        'posts': Post.objects.filter(Q(title__icontains=query) |
                                     Q(content__icontains=query) |
                                     Q(author__username__icontains=query)),
    }
    return render(request, template_name="search.html", context=context)


class MyPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "my_posts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class MyCommentListView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = "my_comments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)


class UserCreateView(generic.CreateView):
    form_class = CustomUserCreateForm
    template_name = "signup.html"
    success_url = reverse_lazy('login')


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = CustomUser
    fields = ['first_name', 'last_name', 'email', 'photo']
    template_name = "profile.html"
    success_url = reverse_lazy('profile')

    def get_object(self, queryset = ...):
        return self.request.user


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'content', 'cover']
    template_name = "form.html"
    success_url = reverse_lazy("posts")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'content', 'cover']
    template_name = "form.html"

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("posts")
    template_name = "delete.html"

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    fields = ['content']
    template_name = "form.html"

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = "delete.html"

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().author == self.request.user