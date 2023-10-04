from http import HTTPStatus

from rest_framework.test import APITestCase, APIClient


class EndpointTestCase(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        super().setUp()
        self.client = APIClient()

    def test_url_access(self):
        """
        Базовый smoke-testing эндпоинтов.
        """

        page_statuses = {
            '/api/v1/files/': HTTPStatus.OK,
            '/api/v1/upload/': HTTPStatus.METHOD_NOT_ALLOWED
        }
        for url, status in page_statuses.items():
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, status)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def tearDown(self):
        super().tearDown()
