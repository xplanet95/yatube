from django.urls import path
from . import views


urlpatterns = [
    # Главная страница
    path("", views.index, name="index"),
    path("new/", views.new_post, name='new_post'),
    path("group/<str:slug>/", views.group_posts, name='group'),
    # Профайл пользователя
    path('profile/<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('profile/<str:username>/<int:post_id>/', views.post_view, name='post'),
    path(
        'profile/<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path("profile/<str:username>/<int:post_id>/comment", views.add_comment, name="add_comment"),

    path("follow/", views.follow_index, name="follow_index"),
    path("profile/<str:username>/follow/", views.profile_follow, name="profile_follow"),
    path("profile/<str:username>/unfollow/", views.profile_unfollow, name="profile_unfollow"),

    path('404/', views.page_not_found),
    path('500/', views.server_error),

    # path('new/', views.CreateNewPost.as_view(), name='new_post'),
]

