from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.utils import IntegrityError

User = get_user_model()


class CreateUserTest(TestCase):
    def setUp(self):
        test_user1 = User.objects.create_user(username='sera2', email='bngnbdjn@mail.com', password='Qq123456')
        test_user1.save()
        test_user2 = User.objects.create_user(username='sera3', email='2bngnbdjn@mail.com', password='Qq123456')
        test_user2.save()

    def test_check_create_test_user(self):
        test_login = self.client.login(username='sera2', password='Qq123456')
        resp = self.client.get(reverse('blog:index'))
        self.assertEquals(str(resp.context['user']), 'sera2')

    def test_create_users_this_same_email(self):
        user1 = User.objects.create_user(username='user10', email='9bngnbdjn@mail.com', password='Qq123456')
        user1.save()

        with self.assertRaises(IntegrityError) as context:
            user2 = User.objects.create_user(username='user11', email='9bngnbdjn@mail.com', password='Qq123456')
            user2.save()

        self.assertTrue('UNIQUE constraint failed' in str(context.exception))



class CloseAccessForNotLoggedUserTest(TestCase):
    def setUp(self) -> None:
        self.test_user1 = User.objects.create_user(username='sera2', email='5bngnbdjn@mail.com', password='Qq123456')
        self.test_user1.save()

    def test_302_if_not_logged_in_profile(self):
        resp = self.client.get(reverse('authentication:profile'))
        self.assertEquals(resp.status_code, 302)

    def test_302_if_not_logged_in_subscribe(self):
        resp = self.client.get(reverse('authentication:subscribe', args=[self.test_user1.id]))
        self.assertEquals(resp.status_code, 302)

    def test_302_if_not_logged_in_unsubscribe(self):
        resp = self.client.get(reverse('authentication:unsubscribe', args=[self.test_user1.id]))
        self.assertEquals(resp.status_code, 302)

    def test_302_if_not_logged_in_subscribe_list(self):
        resp = self.client.get(reverse('authentication:subscribe_list'))
        self.assertEquals(resp.status_code, 302)


class RedirectUserTest(TestCase):
    def setUp(self) -> None:
        user1 = User.objects.create_user(username='user10', email='6bngnbdjn@mail.com', password='Qq123456')
        user1.save()

    def test_redirect_user_after_logout(self):
        login = self.client.login(username='user10', email='7bngnbdjn@mail.com', password='Qq123456')
        print(f'login: {login}')
        resp = self.client.get(reverse('authentication:logout'))
        self.assertRedirects(resp, reverse('blog:index'))
