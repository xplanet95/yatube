from django.test import TestCase, Client
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, Post, Group
from django.core.cache import cache


class UsersPagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': "sarah",
            'email': "connor.s@skynet.com",
            'password': "12345"
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.post('/auth/login/', self.user_data, follow=True)
        self.group = Group.objects.create(title='Собаки', slug='dogs', description='--')

        self.post = Post.objects.create(  # noqa
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.user,
            group=self.group)

        self.urls = [
            '',
            f'/profile/{self.user.username}/',
            f'/profile/{self.user.username}/{self.post.id}/',
            f'/group/{self.post.group.slug}/',
        ]

    def test_profile_page_create(self):
        response = self.client.get(f'/profile/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def test_login_user_can_create_post(self):
        response = self.client.get(reverse('new_post'))
        # self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)

    def test_logout_user_cant_create_post(self):
        self.client.logout()
        response = self.client.get(reverse('new_post'))
        self.assertRedirects(response, '/auth/login/?next=/new/', status_code=302, target_status_code=200,
                             msg_prefix='',
                             fetch_redirect_response=True)

    def test_after_publish_post(self):
        cache.clear()
        for url in self.urls:
            response = self.client.get(url)
            # print(response.content.decode())
            self.assertContains(response, self.post.text.replace('\'', '&#39;'),
                                count=None, status_code=200, msg_prefix='', html=False)

    def test_login_user_can_update_post(self):
        cache.clear()
        response = self.client.get(f'/profile/{self.user.username}/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

        self.post.text = 'New string (up\'dated)'
        self.post.save()
        for url in self.urls:
            response = self.client.get(url)
            self.assertContains(response,
                                self.post.text.replace('\'', '&#39;'),
                                count=None, msg_prefix='',
                                html=False)

    def test_404_page(self):
        response = self.client.get(f'krakazyabra_neponatnaya!!')
        self.assertEqual(response.status_code, 404)

    def test_img_is_inst(self):
        '''появится картинка у поста'''
        cache.clear()
        with open('C:/Dev/Yatube/yatube/media/posts/file.jpg', 'rb') as img:
            # post = self.client.post(reverse('new_post'),
            # {
            #     'author': self.user,
            #     'text': 'post with image',
            #     'group': self.group,
            #     'image': img
            # }, follow=True)
            self.post.text = 'post with image'
            self.post.image = img.name
            self.post.save()
            for url in self.urls:
                response = self.client.get(url)
                self.assertContains(response, f'<img', count=None, msg_prefix='', html=False)

    def test_correct_upload_img(self):
        '''тест что текстовый файл не загрузился в виде картинки,
        как проверить на главной хз, они из кэша грузятся'''
        cache.clear()
        with open('C:/Dev/Yatube/yatube/media/posts/test.txt', 'rb') as img:
            post = Post.objects.create(  # noqa
                text="post with text image",
                author=self.user,
                group=self.group,
                image=img.name)
            urls = [
                f'/profile/{self.user.username}/{self.post.id}/',
            ]
            for url in urls:
                response = self.client.get(url)
                self.assertNotContains(response, f'<img', msg_prefix='', html=False)

    def test_cache_index(self):
        '''подгрузится текст из кэша и на главной текст не обновится'''
        self.post.text = 'cache test'
        self.post.save()
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, self.post.text, msg_prefix='', html=False)