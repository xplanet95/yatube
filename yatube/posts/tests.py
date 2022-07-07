from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Post, Group, Follow, Comment
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
        self.group = Group.objects.create(title='Собаки', slug='dogs', description='--')  # noqa

        self.post = Post.objects.create(  # noqa
            text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
            author=self.user,
            group=self.group)

        self.urls = [
            '',
            reverse('profile', kwargs={'username': self.user.username}),
            reverse('post', kwargs={'username': self.user.username, 'post_id': self.post.id}),
            reverse('group', kwargs={'slug': self.post.group.slug}),
        ]

    def test_profile_page_create(self):
        response = self.client.get(reverse('profile', kwargs={'username': self.user.username}))
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
        response = self.client.get(reverse('post', kwargs={'username': self.user.username, 'post_id': self.post.id}))
        cache.clear()
        # print(response.content.decode())
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
                reverse('post', kwargs={'username': self.user.username, 'post_id': self.post.id}),
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
        cache.clear()
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.post.text, msg_prefix='', html=False)

    def test_login_user_can_follow(self):
        '''селф пользователь подписывается на юзер2, в бд появляется запись и после delete() бд пустая'''
        user_data_2 = {
            'username': "hren",
            'email': "hren@net.com",
            'password': "12345"
        }
        user2 = User.objects.create_user(**user_data_2)
        self.client.get(reverse('profile_follow', kwargs={'username': user2.username}))
        follow = Follow.objects.get(user=User.objects.get(username=self.user.username),  # noqa
                                    author=User.objects.get(username=user2.username))
        self.assertTrue(follow)
        follow.delete()
        self.assertEqual(Follow.objects.all().count(), 0)  # noqa

    def tets_follow_user_view_following(self):
        '''создать пост юзеру2, селф юзер после подписки на юзера2 увидит его пост в ленте избранных,
        создать юзер 3, залогиниться, юзер3 в избранных не увидит поста юзер2 тк не подписан'''
        user_data_2 = {
            'username': "hren",
            'email': "hren@net.com",
            'password': "12345"
        }
        user2 = User.objects.create_user(**user_data_2)
        user_data_3 = {
            'username': "dearq",
            'email': "dearq@net.com",
            'password': "12345"
        }
        user3 = User.objects.create_user(**user_data_3)
        post = Post.objects.create(  # noqa
            text="user 2 post",
            author=user3,
            group=self.group)
        self.client.get(reverse('profile_follow', kwargs={'username': user2.username}))
        response = self.client.get(reverse('follow_index'))
        self.assertContains(response, post.text, msg_prefix='', html=False)
        cache.clear()

        response = self.client.get('')
        self.assertContains(response, post.text, msg_prefix='', html=False)
        cache.clear()

        self.client.logout()
        self.client.post('/auth/login/', user_data_3, follow=True)
        response = self.client.get(reverse('follow_index'))
        self.assertNotContains(response, post.text, msg_prefix='', html=False)

    def test_only_login_user_can_comment(self):
        '''Только авторизованный пользователь сможет оставить коммент'''
        cache.clear()
        comment_data = {'text': 'New comment'}
        self.client.post(reverse('add_comment', kwargs={'username': self.user.username,
                                                        'post_id': self.post.id}), comment_data)
        response = self.client.get(reverse('post', kwargs={'username': self.user.username,
                                                        'post_id': self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertContains(response, Comment.objects.get(id=1).text)

        cache.clear()
        self.client.logout()
        comment_data = {'text': 'New comment 2'}
        self.client.post(reverse('add_comment', kwargs={'username': self.user.username,
                                                        'post_id': self.post.id}), comment_data)
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertNotContains(response, comment_data['text'])
        response = self.client.get(reverse('post', kwargs={'username': self.user.username, 'post_id': self.post.id}))
        self.assertEqual(response.status_code, 404)
