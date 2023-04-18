from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from menu.models import MenuItem, MenuCategory
from reservations.models import Reservation
from datetime import date, timedelta
from decimal import Decimal


class StaffMenuTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = MenuCategory.objects.create(name=MenuCategory.APPETIZERS)
        self.item = MenuItem.objects.create(
            category=self.category,
            name="Something",
            description="Something for testing",
            price=Decimal('12.99')
        )

        self.staff_team = Group.objects.create(name='StaffTeam')
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpassword123'
        )
        self.staff_user.groups.add(self.staff_team)
        self.client.login(username='staffuser', password='testpassword123')

    def test_staff_menu_view(self):
        response = self.client.get('/staff_menu/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Something")


class AllReservationsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.reservation = Reservation.objects.create(
            name="John Doe",
            user_id=1,
            date=date.today() + timedelta(days=3),
            time="17:00",
            party_size=2,
        )

        self.staff_group = Group.objects.create(name='StaffTeam')
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpassword123'
        )
        self.staff_user.groups.add(self.staff_group)
        self.client.login(username='staffuser', password='testpassword123')

    def test_all_reservations_view(self):
        response = self.client.get('/all_reservations/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John Doe")
