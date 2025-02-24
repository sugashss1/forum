from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout', views.user_logout, name='logout'),
    path('create_post', views.create_post, name='create_post'),
    path('reply/<int:post_id>', views.reply, name='reply'),
    path('like/<int:post_id>', views.like_post, name='like_post'),
    path('my_posts/<str:name>', views.my_posts, name='my_posts')
]


