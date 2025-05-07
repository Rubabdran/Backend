from django.test import TestCase
from django.contrib.auth.models import User
from main_app.models import Image, Favorite, Comment
from datetime import datetime

class ModelsTest(TestCase):
    def setUp(self):
        # User
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='otheruser', password='abc123')

        # Images
        self.image1 = Image.objects.create(
            owner=self.user,
            prompt='A cat on Mars',
            image_url='http://example.com/image1.jpg',
            is_public=False
        )
        self.image2 = Image.objects.create(
            owner=self.user,
            prompt='A robot in the forest',
            image_url='http://example.com/image2.jpg',
            is_public=True
        )

        # Favorites
        self.favorite = Favorite.objects.create(user=self.user, image=self.image2)

        # Comments
        self.comment1 = Comment.objects.create(user=self.user, image=self.image1, text='🔥')

    # -------------------
    # Basic creation tests
    # -------------------

    def test_user_create(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_image_create(self):
        self.assertEqual(self.image1.prompt, 'A cat on Mars')
        self.assertEqual(self.image1.owner.username, 'testuser')
        self.assertFalse(self.image1.is_public)
        self.assertEqual(str(self.image1), 'A cat on Mars')

    def test_favorite_create(self):
        self.assertEqual(self.favorite.user, self.user)
        self.assertEqual(self.favorite.image, self.image2)

    def test_comment_create(self):
        self.assertEqual(self.comment1.text, '🔥')
        self.assertEqual(self.comment1.image, self.image1)
        self.assertEqual(self.comment1.user, self.user)

    # -------------------
    # Relationship tests
    # -------------------

    def test_image_owner_relationship(self):
        self.assertEqual(self.image1.owner, self.user)
        self.assertEqual(self.image2.owner, self.user)

    def test_favorite_relationship(self):
        self.assertEqual(self.favorite.image.prompt, 'A robot in the forest')
        self.assertIn(self.favorite, Favorite.objects.filter(user=self.user))

    def test_comment_relationships(self):
        comments = self.image1.comments.all()
        self.assertEqual(comments.count(), 2)
        self.assertIn(self.comment1, comments)
        self.assertIn(self.comment2, comments)

    # -------------------
    # Unique constraint test
    # -------------------

    def test_duplicate_favorite_not_allowed(self):
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.user, image=self.image2)

    # -------------------
    # Cascade delete test
    # -------------------

    def test_image_deletion_cascades(self):
        self.image1.delete()
        self.assertFalse(Comment.objects.filter(image=self.image1.id).exists())

    def test_user_deletion_cascades(self):
        self.other_user.delete()
        self.assertFalse(Comment.objects.filter(user=self.other_user.id).exists())
