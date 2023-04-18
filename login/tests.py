from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from .views import signup, login_view, logout_view, is_staffteam_or_admin
from .forms import CustomUserCreationForm


"""
TEST LOGIN VIEWS
"""

# Test sign up 
class SignUpTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup(self):
        data = {
            'username': 'testuser123',
            'email': 'testuser123@example.com',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!'
        }

        response = self.client.post('/signup/', data)
        # Check user redirected after sign up
        self.assertEqual(response.status_code, 302)


class AuthViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='admin', password='adminpassword')
        self.staff_group = Group.objects.create(name='StaffTeam')
        self.staff = User.objects.create_user(username='staff', password='staffpassword')
        self.staff.groups.add(self.staff_group)

    # Test is_staffteam_or_admin works
    def test_is_staffteam_or_admin(self):
        self.assertFalse(is_staffteam_or_admin(self.user))
        self.assertTrue(is_staffteam_or_admin(self.admin))
        self.assertTrue(is_staffteam_or_admin(self.staff))

    def test_login_view(self):

        # Test login for a regular user
        response = self.client.post('/login/', data={'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/reservations/')

        # Test login for admin user
        response = self.client.post('/login/', data={'username': 'admin', 'password': 'adminpassword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/all_reservations/')

    def test_logout_view(self):

        # Log in
        self.client.login(username='testuser', password='testpassword')

        # Test logout view
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')
