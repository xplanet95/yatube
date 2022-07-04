from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
# from django.views.generic import CreateView
# from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page


@cache_page(20)
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()  # noqa [:11]
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    context = {'page': page, 'paginator': paginator}
    response = render(request, "index.html", context)
    return response


@cache_page(20)
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

@login_required
def new_post(request, post=None):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                text=form.cleaned_data['text'],
                author=request.user,
                group=form.cleaned_data['group'],
                image=form.cleaned_data['image']
            )
            return redirect('index')
    form = PostForm()
    context = {
        'form': form,
        'post': post
    }
    response = render(request, 'new.html', context)
    return response


@cache_page(20)
def profile(request, username):
    profile = get_object_or_404(User, username=request.user)

    author_list_queryset = Follow.objects.filter(user=profile)
    author_list = [author_list_queryset[i].author.username for i in range(len(author_list_queryset))]
    following = User.objects.filter(username__in=author_list)

    username = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author_id=User.objects.get(username=username)).order_by('-pub_date')
    cnt_of_posts = post_list.count()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    context = {'page': page,
               'paginator': paginator,
               'cnt_of_posts': cnt_of_posts,
               'username': username,
               'following': following,
               'profile': profile,
               }
    response = render(request, "profile.html", context)
    return response


@cache_page(20)
def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=request.user)
    author_list_queryset = Follow.objects.filter(user=profile)
    author_list = [author_list_queryset[i].author.username for i in range(len(author_list_queryset))]
    following = User.objects.filter(username__in=author_list)

    profile_id = User.objects.get(username=username)
    post_list = Post.objects.filter(author_id=profile_id)
    post = post_list.get(id=post_id)
    cnt_of_posts = post_list.count()
    comments_list = Comment.objects.filter(post_id=post_id)
    form = CommentForm(instance=None)
    context = {'post': post,
               'cnt_of_posts': cnt_of_posts,
               'username': post.author,
               'form': form,
               'items': comments_list,
               'following': following,
               }
    response = render(request, "post.html", context)
    return response


def add_comment(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            Comment.objects.create(
                post=post,
                author=User.objects.get(username=request.user),
                text=form.cleaned_data['text'])
            return redirect("post", username=username, post_id=post_id)


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)
    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)
    # добавим в form свойство files
    # or None, что бы отрисовывать пустую форму, instance что бы save() обновлял а не создавал
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect("post", username=request.user.username, post_id=post_id)
    context = {'form': form, 'post': post}
    return render(request, 'new.html', context)

    # старый post edit
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    # post = get_object_or_404(Post, id=post_id, author__username=username)
    # if request.method == 'POST':
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         post.text = form.cleaned_data['text']
    #         post.group = form.cleaned_data['group']
    #         post.save()
    #         return redirect('post', username=post.author.username, post_id=post.id)
    #         # redirect(f'/{post.author.username}/{post.id}/')
    # else:
    #     if request.user == post.author:
    #         form = PostForm()
    #         context = {
    #             'form': form,
    #             'post': post,
    #             'username': post.author.username
    #         }
    #         response = render(request, 'new.html', context)
    #         return response
    #     else:
    #         return redirect('post', username=post.author.username, post_id=post.id)
            # redirect(f'/{post.author.username}/{post.id}/')
            # redirect(reverse('post', {'username': username, 'post_id': post.id}))
            # redirect('post', username=username, post_id=post.id)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    profile = get_object_or_404(User, username=request.user.username)
    follow_query_set = Follow.objects.filter(user=profile.id)
    authors_list_user = User.objects.filter(username__in=follow_query_set)
    post_list = Post.objects.filter(author__in=authors_list_user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)
    context = {
        'page': page,
    }
    return render(request, "follow.html", context)


@login_required
def profile_follow(request, username):
    user = User.objects.get(username=request.user.username)
    author = User.objects.get(username=username)
    if not get_object_or_404(Follow, user=user, author=author):
        Follow.objects.create(user=user, author=author)
        author_list_queryset = Follow.objects.filter(user=user)
        author_list = [author_list_queryset[i].author.username for i in range(len(author_list_queryset))]
        User.objects.filter(username__in=author_list)









        # authors_list = Follow.objects.filter(user=User.objects.get(username=request.user.username).id)
        # post_list = Post.objects.filter(author_id=User.objects.get(username=author)).order_by('-pub_date')
        # paginator = Paginator(post_list, 10)
        # cnt_of_posts = post_list.count()
        # page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
        # page = paginator.get_page(page_number)  # получить записи с нужным смещением
        # context = {'page': page,
        #            'paginator': paginator,
        #            'cnt_of_posts': cnt_of_posts,
        #            'username': username,
        #            'following': authors_list,
        #            'profile': author,
        #            }
        # response = render(request, "profile.html", context)
    #     return response
    # return redirect("profile", username=username)








@login_required
def profile_unfollow(request, username):
    user = User.objects.get(username=request.user.username).id
    author = User.objects.get(username=username).id
    Follow.objects.get(user=user, author=author).delete()
