from django.test import TestCase, Client
from .models import User, Post


class UsersPagesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="sarah", email="connor.s@skynet.com", password="12345"
        )
        # post = Post.objects.create(
        #     text="You're talking about things I haven't done yet in the past tense. It's driving me crazy!",
        #     author=self.user)

    def profile_page_create_test(self):
        response = self.client.get(f'/{self.user.username}/')
        self.assertEqual(response.status_code, 200)

    def login_user_can_create_post_test(self):
        response = self.client.get(f'new_post')
        self.assertEqual(response.status_code, 200)

# class TestStringMethods(TestCase):
#     def test_length(self):
#                 self.assertEqual(len('yatube'), 6)
#
#     def test_show_msg(self):
#                 # действительно ли первый аргумент — True?
#                 self.assertTrue(False, msg="Важная проверка на истинность")
