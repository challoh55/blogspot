from django.urls import path
from . import views


urlpatterns = [
    path('', views.homepage, name='home_page'),
    path('register-user/', views.register, name='register_user'),
    path('login-user/', views.Login, name='login_user'),
    path('logout-user/', views.Logout, name='Logout_user'), 
    path('update-profile', views.update_profile, name='update_profile'),
    path('user-homepage/', views.user_homepage, name='user_homepage'),
    path('add-new-post/', views.add_new_post, name='add_new_post'),
    path('delete-post', views.delete_post, name='delete_post'),
    path('update-post', views.update_post, name='update_post'),
    path('view-post-details', views.view_post_details, name='view_post_details'),
    path('all-posts-for-topic', views.all_posts_for_topic, name='all_posts_for_topic'),
    path('like', views.Like_post, name='like_post'),
    path('posts-by-user', views.Posts_by_user, name='posts_by_user'),
]