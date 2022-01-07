from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, RequestsClient, force_authenticate
from rest_framework.authtoken.models import Token

from accounts.models import UserModel
from accounts.views import users

class UserTest(TestCase):

    def setUp(self):
        camilla = User.objects.create(username="Camilla")
        UserModel.objects.create(
            user=camilla, role="staff")

        mandy = User.objects.create(username="Mandy")
        UserModel.objects.create(
            user=mandy, role="admin")
            
    def test_user_case(self):
        camilla = User.objects.get(username='Camilla')
        mandy = User.objects.get(username='Mandy')
        self.assertEqual(
            camilla.usermodel.role, "staff")
        self.assertEqual(
            mandy.usermodel.role, "admin")


class FetchUsersTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='admin', password='admin123')
        self.token = f"Token {Token.objects.create(user=self.user)}"

    def testcase(self):
        factory = APIRequestFactory()
        user = User.objects.get(username="admin")

        request = factory.get("/api/users?role=admin")
        force_authenticate(request, user=user, token=self.token)
        response = users(request)
        self.assertEqual(response.status_code, 200)
