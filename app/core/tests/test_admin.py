from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(   
            email=  "k@gmail.com", password = "pass123"
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="abck@gmail.com", password="pass123",
            name = "test user full name"
        )

    def test_users_listed(self):
        """ Test that users are listed on user page """
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        # print(res)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.admin_user.email)
        print("T----> test admin listing users test passed")

    def test_user_change_page(self):
        """Test that the user edit page works"""
        # i.e when clicking on the id field it directs us 
        # to /admin/core/user/user_id
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        # print(res)
        print("T----> test change user page pass")
