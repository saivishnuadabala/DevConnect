from django.urls import path
from .views import register, user_login, user_logout, home, create_post,like_post,comment_post,delete_post

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("", user_login, name="login"),
    path("home",home,name='home'),
    path("create_post/", create_post, name="create_post"),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
]
urlpatterns += [
    path("like/<int:post_id>/", like_post, name="like_post"),
    path("comment/<int:post_id>/", comment_post, name="comment_post"),
]
