from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Tag
from unittest.mock import patch
from core import models

def create_sample_user(email="khed@g.com", password="abcdf54651"):
    """ create a dummy sample user for our test """
    return get_user_model().objects.create(email = email, password = password)
    


class ModelTests(TestCase):
    """  A class for testing models instance creation """

    def test_create_user_model_with_email(self):
        email = "k@gmail.com"
        password = "TEstPassword1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        ## check passing the test case 
        self.assertEqual(email , user.email)
        self.assertTrue(user.check_password(password))
        
        print("T----> Creating user test passed")


    def test_new_user_invalid_email(self):
        """Test creating user with no email or invlid email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("assb.com", 'test123')
        print("T----> Creating user with invalid email  test passed")

    def test_tag_str(self):
        tag = Tag.objects.create(
            user = create_sample_user(),
            name = "Meat"
        )
        self.assertEqual(str(tag), tag.name)
        print("T----> test tag str representation passed")


    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that uploaded images are saved in the correct location """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_img_file_path(None, 'image.jpg')

        exp_path = f'uploads/recipes/{uuid}.jpg'
        self.assertEqual(file_path, exp_path )

