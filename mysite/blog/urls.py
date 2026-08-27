from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name="posts"),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name="post"),
    path('search/', views.search, name='search'),
    path('myposts/', views.MyPostListView.as_view(), name="my_posts"),
    path('mycomments/', views.MyCommentListView.as_view(), name="my_comments"),
    path('profile/', views.UserUpdateView.as_view(), name="profile"),
    path('signup/', views.UserCreateView.as_view(), name="signup"),
    path("posts/create/", views.PostCreateView.as_view(), name="post_create"),
]
