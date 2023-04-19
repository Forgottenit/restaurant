from django.test import TestCase, Client
from .models import MenuCategory, MenuItem
from decimal import Decimal
from django.contrib.auth.models import User, Group

"""
TEST Menu models
"""


# Test Menu Category
class MenuCategoryTestCase(TestCase):
    def test_create_menu_category(self):
        category = MenuCategory.objects.create(name=MenuCategory.APPETIZERS)
        self.assertEqual(category.name, MenuCategory.APPETIZERS)
        self.assertEqual(str(category), MenuCategory.APPETIZERS)


# Test Menu Item
class MenuItemTestCase(TestCase):
    def setUp(self):
        self.category = MenuCategory.objects.create(
                                        name=MenuCategory.APPETIZERS)

    def test_create_menu_item(self):
        item = MenuItem.objects.create(
            category=self.category,
            name="Something",
            description="Something for testing.",
            price=Decimal('12.99')
        )

        self.assertEqual(item.category, self.category)
        self.assertEqual(item.name, "Something")
        self.assertEqual(item.description, "Something for testing.")
        self.assertEqual(item.price, Decimal('12.99'))
        self.assertEqual(str(item), "Something")


"""
TEST MENU views
"""


class MenuViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = MenuCategory.objects.create(
                                        name=MenuCategory.APPETIZERS)
        self.item = MenuItem.objects.create(
            category=self.category,
            name="Something",
            description="Something for testing.",
            price=Decimal('12.99')
        )

    def test_menu_view(self):
        response = self.client.get('/menu/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Something")


class StaffMenuViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = MenuCategory.objects.create(
                                    name=MenuCategory.APPETIZERS)
        self.item = MenuItem.objects.create(
            category=self.category,
            name="Something",
            description="Something for testing",
            price=Decimal('12.99')
        )

        self.staff_group = Group.objects.create(name='StaffTeam')
        self.staff_user = User.objects.create_user(
            username='staffuser',
            password='testpass123'
        )
        self.staff_user.groups.add(self.staff_group)
        self.client.login(username='staffuser', password='testpass123')

    def test_create_menu_item(self):
        response = self.client.post('/create_menu_item/', {
            'category': self.category.id,
            'name': 'Something new',
            'description': 'Something new',
            'price': '14.99'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MenuItem.objects.filter(name='Something new').exists())

    def test_edit_menu_item(self):
        response = self.client.post(f'/edit_menu_item/{self.item.id}/', {
            'category': self.category.id,
            'name': 'Edited item',
            'description': 'edited item',
            'price': '15.99'
        })
        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Edited item')

    def test_delete_menu_item(self):
        response = self.client.post(f'/delete_menu_item/{self.item.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(MenuItem.objects.filter(id=self.item.id).exists())
