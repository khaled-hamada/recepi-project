from django.test import TestCase
from django.contrib.auth import get_user_model

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
