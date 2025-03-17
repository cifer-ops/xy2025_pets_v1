from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserProfile
from .forms import LoginForm, RegisterForm
import os
import sys

# Set up the Django environment so that the test can run independently
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xy_pets.settings')
import django
django.setup()

# Create your tests here.

class UserModelTest(TestCase):
    """User model testing"""
    
    def setUp(self):
        """Set up test data"""
        self.user = UserProfile.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            mobile='13800138000'
        )
    
    def test_user_creation(self):
        """Test user creation"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.mobile, '13800138000')
        self.assertTrue(self.user.check_password('testpassword123'))
    
    def test_user_str_method(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')


class LoginViewTest(TestCase):
    """Login view test"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.login_url = reverse('login')
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
    
    def test_login_view_get(self):
        """Test the GET request login page"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_view_post_success(self):
        """Test successfully logged in"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect status code
        
    def test_login_view_post_invalid(self):
        """Invalid test login"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Incorrect username or password")


class RegisterFormTest(TestCase):
    """Registration form test"""
    
    def test_valid_form(self):
        """Test valid registration form"""
        form_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'password2': 'newpassword123',
            'mobile': '13900139000'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """Test password mismatch"""
        form_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'password2': 'differentpassword',
            'mobile': '13900139000'
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

if __name__ == '__main__':
    import unittest
    unittest.main()
