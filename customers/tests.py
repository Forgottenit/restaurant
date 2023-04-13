from django.test import Client, TestCase
from customers import views

class ErrorHandlersTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_error_403_view(self):
        response = self.client.get('/403/')
        self.assertEqual(response.status_code, 403)

    def test_error_404_view(self):
        response = self.client.get('/404/')
        self.assertEqual(response.status_code, 404)

    def test_error_500_view(self):
        response = self.client.get('/500/')
        self.assertEqual(response.status_code, 500)

class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class AboutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_about_view(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

class ErrorTemplateTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_404_template(self):
        response = self.client.get('/trigger-404/')
        self.assertContains(response, 'Page not found', status_code=404)

    def test_403_template(self):
        response = self.client.get('/trigger-403/')
        self.assertContains(response, 'Forbidden', status_code=403)
