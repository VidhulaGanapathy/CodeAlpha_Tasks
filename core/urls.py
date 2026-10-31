from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('user/<str:username>/', views.profile, name='profile'),
    path('user/<str:username>/follow/', views.follow_user, name='follow'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('user/<str:username>/followers/', views.follow_list, {'kind': 'followers'}, name='followers'),
    path('user/<str:username>/following/', views.follow_list, {'kind': 'following'}, name='following'),
]