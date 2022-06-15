from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Group
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
    post_list = group.posts.all().order_by("-pub_date").all()  # [:12]
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
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                text=form.cleaned_data['text'],
                author=request.user,
                group=form.cleaned_data['group']
            )
            return redirect('index')
        context = {
            'form': form,
        }
        response = render(request, 'new.html', context)
        return response
    else:
        form = PostForm()
        context = {
            'form': form,
        }
        response = render(request, 'new.html', context)
        return response


def profile(request, username):
        # тут тело функции
        return render(request, 'profile.html', {})


def post_view(request, username, post_id):
    # тут тело функции
    return render(request, 'post.html', {})


def post_edit(request, username, post_id):
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)
    return render(request, 'new.html', {})