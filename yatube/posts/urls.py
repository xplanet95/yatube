from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Главная страница
    path("", views.index, name="index"),
    path("new/", views.new_post, name='new_post'),
    path("group/<str:slug>/", views.group_posts),
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
    path('404/', views.page_not_found),
    path('500/', views.server_error),

    # path('new/', views.CreateNewPost.as_view(), name='new_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
