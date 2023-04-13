from django.test import RequestFactory, TestCase

# Create your tests here.


class ErrorHandlersTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_error_403_view(self):
        request = self.factory.get('/some-page/')
        response = views.error_403(request, exception=None)
        self.assertEqual(response.status_code, 403)

    def test_error_404_view(self):
        request = self.factory.get('/some-page/')
        response = views.error_404(request, exception=None)
        self.assertEqual(response.status_code, 404)

    def test_error_500_view(self):
        request = self.factory.get('/some-page/')
        response = views.error_500(request)
        self.assertEqual(response.status_code, 500)