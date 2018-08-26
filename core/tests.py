from django.contrib.auth.models import User
from core.models import Assignee, Organization, Task
from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase


class AuthorizationTestCase(APITestCase):
    signin_url = reverse("api:signin")
    signout_url = reverse("api:signout")

    def setUp(self):
        self.email = "testuser_001@example.com"
        self.username, self.company = self.email.split("@")
        self.password = "123qwe123"

        self.user = User.objects.create_user(self.username, email=self.email, password=self.password)
        self.organization1 = Organization.objects.create(name=self.company)
        self.organization2 = Organization.objects.create(name=self.company+"2")
        self.assignee = Assignee.objects.create(user=self.user)
        self.assignee.organization.add(self.organization1)

    def test_correct_datas(self):
        data = {
            "email": self.email,
            "organiz": self.company,
            "passw": self.password
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(200, response.status_code)
        response = self.client.get(self.signout_url)
        self.assertEqual(200, response.status_code)

    def test_invalid_organization(self):
        data = {
            "email": self.email,
            "organiz": self.company + "2",
            "passw": self.password
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(404, response.status_code)

    def test_invalid_email(self):
        data = {
            "email": "c" + self.email,
            "organiz": self.company,
            "passw": self.password
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(404, response.status_code)

    def test_invalid_passw(self):
        data = {
            "email": self.email,
            "organiz": self.company,
            "passw": self.password + "1"
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(404, response.status_code)


class CRUDTaskTestCase(APITestCase):
    signin_url = reverse("api:signin")
    signout_url = reverse("api:signout")
    tasks_url = reverse("api:tasks-list")

    def setUp(self):
        self.email = "testuser_002@example2.com"
        self.username, self.company = self.email.split("@")
        self.password = "123qwe123"

        self.user = User.objects.create_user(self.username, email=self.email, password=self.password)
        self.organization = Organization.objects.create(name=self.company)
        self.assignee = Assignee.objects.create(user=self.user)
        self.assignee.organization.add(self.organization)

        self.client.post(self.signin_url, {"email": self.email, "organiz": self.company, "passw": self.password})
        self.data = {
            "name": "Проверить тестовое задание 1",
            "description": "Описание для тестового задания 1",
            "deadline": "2018-08-26T17:25:29Z",
            "status": 1,
            "priority": 1
        }
        response = self.client.post(self.tasks_url, self.data)
        self.task_pk = response.data.get("id")
        self.client.get(self.signout_url)

    def test_create_task(self):
        self.client.post(self.signin_url, {"email": self.email, "organiz": self.company, "passw": self.password})
        data = {
            "name": "Проверить тестовое задание 2",
            "description": "Описание для тестового задания 2",
            "deadline": "2018-08-26T17:25:29Z",
            "status": 1,
            "priority": 1
        }
        response = self.client.post(self.tasks_url, data)
        self.assertEqual(201, response.status_code)
        response = self.client.get(self.signout_url)
        self.assertEqual(200, response.status_code)
        self.client.get(self.signout_url)

    def test_read_task(self):
        self.client.post(self.signin_url, {"email": self.email, "organiz": self.company, "passw": self.password})
        response = self.client.get(self.tasks_url)
        data = {
            "name": response.data[0].get("name"),
            "description": response.data[0].get("description"),
            "deadline": response.data[0].get("deadline"),
            "status": response.data[0].get("status"),
            "priority": response.data[0].get("priority")
        }
        self.assertEqual(self.data, data)
        self.client.get(self.signout_url)

    def test_update_task(self):
        response = self.client.post(self.signin_url, {"email": self.email, "organiz": self.company, "passw":
                                    self.password})
        self.assertEqual(200, response.status_code)

        self.data.update({"description": "Измененное описание"})
        response = self.client.put("%s%d/" % (self.tasks_url, self.task_pk), self.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("Измененное описание", response.data.get("description"))
        self.client.get(self.signout_url)

    def test_delete_task(self):
        self.client.post(self.signin_url, {"email": self.email, "organiz": self.company, "passw": self.password})
        response = self.client.delete("%s%d/" % (self.tasks_url, self.task_pk))
        self.assertEqual(204, response.status_code)
        self.client.get(self.signout_url)


class TwoCompanyTestCase(APITestCase):
    signin_url = reverse("api:signin")
    signout_url = reverse("api:signout")
    tasks_url = reverse("api:tasks-list")

    def setUp(self):
        self.email = "testuser_003@example.com"
        self.username = "testuser_003"
        self.company1 = "mydearcomp1"
        self.company2 = "mydearcomp2"
        self.password = "123qwe123"

        self.user = User.objects.create_user(self.username, email=self.email, password=self.password)
        self.organization1 = Organization.objects.create(name=self.company1)
        self.organization2 = Organization.objects.create(name=self.company2)
        self.assignee = Assignee.objects.create(user=self.user)
        self.assignee.organization.add(self.organization1, self.organization2)

    def test_wo_authorization(self):
        response = self.client.get(self.tasks_url)
        self.assertEqual(403, response.status_code)

    def test_two_task(self):
        self.client.post(self.signin_url, {"email": self.email, "organiz": self.company1, "passw": self.password})
        data = {"name": "123", "description": "", "deadline": "", "status": 2, "priority": 2}
        response = self.client.post(self.tasks_url, data)
        self.assertEqual(201, response.status_code)
        self.client.get(self.signout_url)

        self.client.post(self.signin_url, {"email": self.email, "organiz": self.company2, "passw": self.password})
        response = self.client.post(self.tasks_url, data)
        self.assertEqual(201, response.status_code)

        self.assertEqual(2, Task.objects.all().count())

        response = self.client.get(self.tasks_url)
        self.assertEqual(1, len(response.data))
