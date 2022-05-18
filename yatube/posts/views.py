from django.shortcuts import render, get_object_or_404
from .models import Post, Group


def index(request):
    latest = Post.objects.all()[:11]
    context = {"posts": latest}
    response = render(request, "index.html", context)
    return response

def group_posts(request, slug):
    # функция get_object_or_404 получает по заданным критериям объект из базы данных
    # или возвращает сообщение об ошибке, если объект не найден
    group = get_object_or_404(Group, slug=slug)

    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # условия WHERE group_id = {group_id}
    #  posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    posts = group.posts.all().order_by("-pub_date")[:12]
    context = {"group": group, "posts": posts}
    return render(request, "group.html", context)