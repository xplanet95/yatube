from django.shortcuts import render,redirect , get_object_or_404
from .models import Post, Group
from .forms import PostForm


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


def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm()
        context = {
            'form': form
        }
        response = render(request, 'new.html', context)
        return