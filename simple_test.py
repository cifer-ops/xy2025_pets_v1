#!/usr/bin/env python
"""A very simple test script that only tests the most basic functions of the UserProfile model
No dependency on the Django test framework, implementing minimal test dependencies"""
import sys
import os
import django
from django.conf import settings
import unittest
import uuid

# Configure the Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Minimalist configuration, including only necessary settings
config = {
    'DEBUG': True,
    'INSTALLED_APPS': [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'accounts',
    ],
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    'AUTH_USER_MODEL': 'accounts.UserProfile',
}

print("Configure the Django environment...")
# Application configuration
settings.configure(**config)
django.setup()

# Import the model to be tested
from accounts.models import UserProfile

class UserModelSimpleTest(unittest.TestCase):
    """Simple test of user model"""
    
    def setUp(self):
        """Set up test data"""
        print("\nSet test data...")
        # Make sure the database table is created
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # Create test users and ensure uniqueness with random suffixes
        unique_suffix = str(uuid.uuid4())[:8]
        self.username = f'testuser_{unique_suffix}'
        self.email = f'test_{unique_suffix}@example.com'
        self.mobile = f'138{unique_suffix}'
        
        self.user = UserProfile.objects.create_user(
            username=self.username,
            email=self.email,
            password='testpassword123',
            mobile=self.mobile
        )
        print(f"Created test user: {self.username}")
    
    def test_user_creation(self):
        """Test user creation"""
        print("Execute test: test_user_creation")
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.mobile, self.mobile)
        self.assertTrue(self.user.check_password('testpassword123'))
        print("Test passed: The user creation function works normally")
    
    def test_user_str_method(self):
        """Test user string representation"""
        print("Execute test: test_user_str_method")
        self.assertEqual(str(self.user), self.username)
        print("Test passed: The user string representation method works normally")

if __name__ == '__main__':
    print("Start testing...")
    unittest.main(verbosity=2) 