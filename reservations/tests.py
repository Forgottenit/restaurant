from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, time, timedelta
from .forms import BookingForm
from .models import Reservation
from unittest.mock import patch
from django.urls import reverse
from .views import reservations, user_reservations, delete_reservation, edit_reservation



"""
TESTS FOR FORMS.PY
"""
class BookingFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_valid_form(self):
        # Test that a valid form submission passes validation
        form = BookingForm({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': (timezone.now() + timedelta(days=1)).date(),
            'time': '17:00',
            'party_size': 4,
            'special_requests': 'Some special requests'
        }, user=self.user)

        self.assertTrue(form.is_valid())

    @patch('reservations.forms.MAX_CAPACITY', 4)
    def test_exceeding_capacity(self):
        # Test that a form submission exceeding the restaurant's max capacity fails validation
        form = BookingForm({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': (timezone.now() + timedelta(days=1)).date(),
            'time': '17:00',
            'party_size': 5,
            'special_requests': 'Some special requests'
        }, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('party_size', form.errors)

    def test_past_date(self):
        # Test that a form submission with a past date fails validation
        form = BookingForm({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': (timezone.now() - timedelta(days=1)).date(),
            'time': '17:00',
            'party_size': 4,
            'special_requests': 'Some special requests'
        }, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_past_time(self):
        # Test that a form submission with a past time on the current date fails validation
        form = BookingForm({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': timezone.now().date(),
            'time': '00:00',
            'party_size': 4,
            'special_requests': 'Some special requests'
        }, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('time', form.errors)

    def test_existing_reservation(self):
        # Test that a form submission with the same date and time as an existing reservation fails validation
        Reservation.objects.create(
            user=self.user,
            name='John Doe',
            email='john.doe@example.com',
            date=(timezone.now() + timedelta(days=1)).date(),
            time=time(hour=17),
            party_size=4,
            special_requests='Some special requests'
        )

        form = BookingForm({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': (timezone.now() + timedelta(days=1)).date(),
            'time': '17:00',
            'party_size': 4,
            'special_requests': 'Some special requests'
        }, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    @patch('reservations.forms.BookingForm.guests_during_booking', return_value=48)
    def test_exceeding_capacity(self, mock_guests_during_booking):
        # Test that a form submission exceeding the restaurant's capacity fails validation
        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': (timezone.now() + timedelta(days=1)).date(),
            'time': '17:00',
            'party_size': 5,
            'special_requests': 'Some special requests'
        }

        form = BookingForm(form_data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('party_size', form.errors)

    def test_within_capacity(self):
        # Test that a form submission matching the restaurant's capacity passes validation
        # Create 9 reservations with a party size of 5, leaving room for one more reservation
        for i in range(9):
            Reservation.objects.create(
                user=User.objects.create_user(
                    username=f'testuser{i}',
                    password='testpassword'
                ),
                name='John Doe',
                email='john.doe@example.com',
                date=(timezone.now() + timedelta(days=50)).date(),
                time=time(hour=17),
                party_size=5,
                special_requests='Some special requests'
            )

        form = BookingForm({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': (timezone.now() + timedelta(days=50)).date(),
            'time': '17:00',
            'party_size': 5,
            'special_requests': 'Some special requests'
        }, user=self.user)

        self.assertTrue(form.is_valid())

    def test_double_booking(self):
        # Test that a user can't make two bookings on the same day
        # Create an existing reservation
        existing_reservation = Reservation.objects.create(
            user=self.user,
            name='John Doe',
            email='john.doe@example.com',
            date=(timezone.now() + timedelta(days=60)).date(),
            time='17:00',
            party_size=2,
        )

        # Attempt to create another reservation with the same date and different time
        form = BookingForm({
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': existing_reservation.date,
            'time': '18:00',
            'party_size': 3,
            'special_requests': 'Some special requests'
        }, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn('date', form.errors)

    def test_form_submission(self):
        # Test that a valid form submission creates a new reservation with the correct details
        form_data = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'date': (timezone.now() + timedelta(days=2)).date(),
            'time': '17:00',
            'party_size': 4,
            'special_requests': 'Some special requests'
        }

        form = BookingForm(form_data, user=self.user)

        self.assertTrue(form.is_valid())
        reservation = form.save(commit=False)
        reservation.user = self.user
        reservation.save()

        created_reservation = Reservation.objects.get(user=self.user, date=form_data['date'])

        self.assertEqual(created_reservation.name, form_data['name'])
        self.assertEqual(created_reservation.email, form_data['email'])
        self.assertEqual(created_reservation.time.strftime("%H:%M"), form_data['time'])
        self.assertEqual(created_reservation.party_size, form_data['party_size'])
        self.assertEqual(created_reservation.special_requests, form_data['special_requests'])


"""
TESTS FOR VIEWS.PY
"""


class TestReservationsViews(TestCase):

    def setUp(self):
        # Set up test data and objects for use in tests
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.reservation = Reservation.objects.create(
            user=self.user,
            name='John Doe',
            email='john.doe@example.com',
            date=timezone.now().date() + timedelta(days=1),
            time='17:00:00',
            party_size=2
        )

    def test_reservations_view_logged_out(self):
        # Test that logged_out users are redirected (302 STATUS) when trying to accessreservations view
        response = self.client.get(reverse('reservations'))
        self.assertEqual(response.status_code, 302)

    def test_reservations_view_logged_in(self):
        # Test that logged_in users can access the reservations view and that correct template used
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservations.html')
        self.assertIsInstance(response.context['form'], BookingForm)

    def test_user_reservations_view_logged_out(self):
        # Test that logged_out users are redirected (302 STATUS) when trying to access user_reservations view
        response = self.client.get(reverse('user_reservations'))
        self.assertEqual(response.status_code, 302)

    def test_user_reservations_view_logged_in(self):
        # Test that logged_in users can access the user_reservations view and that correct template used
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_reservations'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'successful_booking.html')

    def test_delete_reservation_view_logged_out(self):
        # Test that logged_out users are redirected when trying to access delete_reservation view
        response = self.client.get(reverse('delete_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 302)

    def test_delete_reservation_view_logged_in(self):
        # Test that logged_in users can delete a reservation and are redirected to successful_booking 
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('delete_reservation', args=[self.reservation.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'successful_booking.html')
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    def test_edit_reservation_view_logged_out(self):
        # Test that logged_out users are redirected (302 STATUS) when trying to access edit_reservation view
        response = self.client.get(reverse('edit_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 302)

    def test_edit_reservation_view_logged_in(self):
        # Test that logged_in users can access the edit_reservation view and that correct template is used
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('edit_reservation', args=[self.reservation.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_reservation.html')
        self.assertIsInstance(response.context['form'], BookingForm)
