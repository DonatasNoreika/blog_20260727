from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name="posts"),
    path('posts/<int:pk>/', views.post, name="post"),
]
