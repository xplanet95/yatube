from django.urls import path

from . import views

urlpatterns = [
    # Главная страница
    path("", views.index, name="index"),
    path("new/", views.new_post, name='new_post'),
    # Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),
    # Просмотр записи
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    path(
        '<str:username>/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path("group/<str:slug>/", views.group_posts),

    # path('new/', views.CreateNewPost.as_view(), name='new_post'),
]