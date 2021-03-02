from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый текст',
            slug='test-slug'
        )

        cls.user = User.objects.create(
            username='Тестовый автор'
        )

        Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'index.html': reverse('index'),
            'new.html': reverse('new_post'),
            'group.html': (
                reverse('group_posts', kwargs={'slug': 'test-slug'})
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('index'))
        post_text_0 = response.context.get('posts')[0].text
        post_author_0 = response.context.get('posts')[0].author
        post_group_0 = response.context.get('posts')[0].group
        self.assertEqual(post_text_0, 'Тестовый текст', post_text_0)
        self.assertEqual(post_author_0.username, 'Тестовый автор',
                         post_text_0)
        self.assertEqual(post_group_0.title, 'Тестовый заголовок',
                         post_group_0)

    def test_group_page_show_correct_context(self):
        """Шаблон group_posts сформирован с правильным контекстом"""
        response = self.authorized_client.get(
            reverse('group_posts', kwargs={'slug': 'test-slug'})
        )
        self.assertEqual(response.context['group'].title,
                         'Тестовый заголовок')
        self.assertEqual(response.context['group'].description,
                         'Тестовый текст')
        self.assertEqual(response.context['posts'][0].text, 'Тестовый текст')
        self.assertEqual(response.context['posts'][0].author.username,
                         'Тестовый автор')

    def test_new_page_show_correct_context(self):
        """Шаблон new_page сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('new_post'))
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_is_in_right_group(self):
        """"Пост попал в правильную группу"""
        Group.objects.create(
            title='Тестовый заголовок',
            description='Тестовый текст',
            slug='test-slug2'
        )
        response = self.authorized_client.get(reverse(
            'group_posts', kwargs={'slug': 'test-slug'})
        )
        self.assertEqual(len(response.context['posts']), 1)
        response = self.authorized_client.get(reverse(
            'group_posts', kwargs={'slug': 'test-slug2'})
        )
        self.assertEqual(len(response.context['posts']), 0)
