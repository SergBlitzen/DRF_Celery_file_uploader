from http import HTTPStatus

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient

from files.models import File


class ViewsTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_file = SimpleUploadedFile("test_file.txt", b"test_content")

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_file_upload(self):
        """
        Проверка создания объекта по POST-запросу.
        """
        url = '/api/v1/upload/'
        test_data = {
            'file': ViewsTestCase.test_file
        }
        initial_objects_count = File.objects.count()
        self.assertEqual(initial_objects_count, 0)

        response = self.client.post(url, test_data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        new_objects_count = File.objects.count()
        self.assertEqual(new_objects_count, 1)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def tearDown(self):
        super().tearDown()
