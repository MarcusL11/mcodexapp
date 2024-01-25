from django.urls import path
from . import views 

urlpatterns = [
    path("", views.home, name='home'),
    path("blogpage/<slug:slug>/", views.blogpage, name='blogpage'),
    path("categories/<str:tag_id>/", views.categories, name='categories'),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("update_profile_pic/", views.update_profile_pic, name="update_profile_pic"),

    
]
