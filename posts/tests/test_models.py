from django.test import TestCase
from django.contrib.auth import get_user_model

from posts.models import Post, Group


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Ж' * 100,
            description='Тестовый текст',
        )

    def test_group_is_title_field(self):
        """__str__  task - это строчка с содержимым task.title."""
        task = GroupModelTest.group
        expected_object_name = task.title
        self.assertEquals(expected_object_name, str(task))


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        User = get_user_model()
        cls.user = User.objects.create()

        cls.post = Post.objects.create(
            text='Ж' * 100,
            author=cls.user,
        )

    def test_post_is_title_field(self):
        """__str__  task - это строчка с содержимым task.title."""
        task = PostModelTest.post
        expected_object_name = task.text[:15]
        self.assertEquals(expected_object_name, str(task)[:15])
