from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Group, User
from .forms import PostForm
from django.core.paginator import Paginator
# from django.views.generic import CreateView
# from django.urls import reverse_lazy


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()  # [:11]
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    context = {'page': page, 'paginator': paginator}
    response = render(request, "index.html", context)
    return response


def group_posts(request, slug):
    # функция get_object_or_404 получает по заданным критериям объект из базы данных
    # или возвращает сообщение об ошибке, если объект не найден
    group = get_object_or_404(Group, slug=slug)
    # Метод .filter позволяет ограничить поиск по критериям. Это аналог добавления
    # условия WHERE group_id = {group_id}
    #  posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    post_list = group.posts.order_by("-pub_date").all()  # [:12]
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {"group": group, 'page': page, 'paginator': paginator}
    return render(request, "group.html", context)


# class CreateNewPost(CreateView):
#     form_class = PostForm
#     template_name = 'new.html'
#     success_url = reverse_lazy('index')

def new_post(request):
    post = ''
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                text=form.cleaned_data['text'],
                author=request.user,
                group=form.cleaned_data['group']
            )
            return redirect('index')
    else:
        form = PostForm()
        context = {
            'form': form,
            'post': post
        }
        response = render(request, 'new.html', context)
        return response


def profile(request, username):
    # username = request.user
    post_list = Post.objects.filter(author_id=User.objects.get(username=username)).order_by('-pub_date')
    cnt_of_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    context = {'page': page,
               'paginator': paginator,
               'cnt_of_posts': cnt_of_posts}
    response = render(request, "profile.html", context)
    return response


def post_view(request, username, post_id):
    post_list = Post.objects.filter(author_id=User.objects.get(username=username))
    post = post_list.get(id=post_id)
    cnt_of_posts = post_list.count()
    context = {'post': post, 'cnt_of_posts': cnt_of_posts}
    response = render(request, "post.html", context)
    return response


def post_edit(request, username, post_id):
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    post_list = Post.objects.filter(author_id=User.objects.get(username=username))
    post = post_list.get(id=post_id)
    if request.method == 'POST' and request.user == post.author:
        form = PostForm(request.POST)
        if form.is_valid():
            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.save()
            return redirect('index')
    else:
        form = PostForm()
        context = {
            'form': form,
            'post': post
        }
        response = render(request, 'new.html', context)
    return response
