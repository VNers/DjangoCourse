from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .signals import pre_save_handler
from SungrillaClub import settings
from .models import Category, Product, Cart, CartItem, ActionLog


class CartModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            portion_size='Test Portion Size',
            price=9.99,
            image='test_image.jpg'
        )

        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user, total_price=0.00)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.total_price, 0.00)
        self.assertIsNotNone(cart.created_at)

        cart_item = CartItem.objects.create(cart=cart, product=self.product, quantity=2, total_price=19.98)
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.total_price, 19.98)


class CartViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            portion_size='Test Portion Size',
            price=9.99,
            image='test_image.jpg'
        )
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('add_to_cart', kwargs={'product_id': self.product.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart'))

        cart = Cart.objects.get(user=self.user)

        cart_items = CartItem.objects.filter(cart=cart)
        self.assertEqual(cart_items.count(), 1)

        cart_item = cart_items.first()
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 1)


class CSRFProtectionTestCase(TestCase):
    def test_csrf_protection(self):
        response = self.client.post(reverse('booking'), {'data': 'product'})
        self.assertEqual(response.status_code, 200)


class SecuritySettingsTestCase(TestCase):
    def test_session_cookie_security(self):
        self.assertTrue(settings.CSRF_COOKIE_SECURE, "Expected CSRF_COOKIE_SECURE to be True.")
        self.assertTrue(settings.SESSION_COOKIE_SECURE, "Expected SESSION_COOKIE_SECURE to be True.")

        self.assertEqual(settings.SESSION_COOKIE_NAME, 'session_id')

    def test_x_frame_options(self):
        self.assertEqual(settings.X_FRAME_OPTIONS, 'DENY')


class ActionLogSignalsTestCase(TestCase):
    def test_pre_save_handler(self):
        action_log = ActionLog.objects.create(
            content_type=None,
            object_id=None,
            object_repr='Test Action Log',
            action_flag=CHANGE
        )
        log_entry_count_before = LogEntry.objects.count()

        pre_save_handler(sender=ActionLog, instance=action_log)

        log_entry_count_after = LogEntry.objects.count()
        self.assertEqual(log_entry_count_after, log_entry_count_before + 0)

    def test_pre_delete_handler(self):
        action_log = ActionLog.objects.create(
            content_type=None,
            object_id=None,
            object_repr='Test Action Log',
            action_flag=CHANGE
        )
        log_entry_count_before = LogEntry.objects.count()

        action_log.delete()

        log_entry_count_after = LogEntry.objects.count()
        self.assertEqual(log_entry_count_after, log_entry_count_before + 1)