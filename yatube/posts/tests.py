from django.test import TestCase, Client
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import User, Post, Group


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
        urls = ['', f'/profile/{self.user.username}/', f'/profile/{self.user.username}/{self.post.id}/']
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, self.post.text.replace('\'', '&#39;'), count=None, msg_prefix='', html=False)

    def test_login_user_can_update_post(self):
        response = self.client.get(f'/profile/{self.user.username}/{self.post.id}/')
        self.assertEqual(response.status_code, 200)

        self.post.text = 'New string (up\'dated)'
        self.post.save()
        urls = ['', f'/profile/{self.user.username}/', f'/profile/{self.user.username}/{self.post.id}/']
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response,
                                self.post.text.replace('\'', '&#39;'),
                                count=None, msg_prefix='',
                                html=False)

    def test_404_page(self):
        response = self.client.get(f'krakazyabra_neponatnaya!!')
        self.assertEqual(response.status_code, 404)

    def test_img_is_inst(self):
        with open('media/posts/file.jpg', 'rb') as img:
            self.post = self.client.post(f'/profile/{self.user.username}/{self.post.id}/edit/',
                {
                    'author': self.user,
                    'text': 'post with image',
                    'group': self.group,
                    'image': img
                }, follow=True)
        self.assertEqual(self.post.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
        urls = [
            '',
        #     f'/profile/{self.user.username}/',
        #     # f'/profile/{self.user.username}/{self.post.id}/',
        #     # f'/group/{self.post.group.slug}/',
        ]
        for url in urls:
            response = self.client.get(url)
            self.assertContains(response, f'<img', count=None, msg_prefix='', html=False)

        # self.assertIn(post.text, response.content)
            # self.assertEqual(response.content, post.text)
# class TestStringMethods(TestCase):
#     def test_length(self):
#                 self.assertEqual(len('yatube'), 6)
#
#     def test_show_msg(self):
#                 # действительно ли первый аргумент — True?
#                 self.assertTrue(False, msg="Важная проверка на истинность")
