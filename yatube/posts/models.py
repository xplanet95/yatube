from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='Текст записи')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  # author_posts
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="posts",  # group_posts
                              blank=True, null=True, verbose_name='Группа')
    # поле для картинки
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return self.text


class Meta:
    ordering = ['-pub_date']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ['-created']


