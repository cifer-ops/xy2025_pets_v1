#!/usr/bin/env python
"""A very simple test script that only tests the most basic functions of PetsInfo and PetsType models
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
        'pets',
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
from pets.models import PetsType, PetsInfo

class PetsModelSimpleTest(unittest.TestCase):
    """Simple test of pet model"""
    
    def setUp(self):
        """Set up test data"""
        print("\nSet test data...")
        # Make sure the database table is created
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # Create a unique test user
        unique_suffix = str(uuid.uuid4())[:8]
        self.username = f'testuser_{unique_suffix}'
        self.user = UserProfile.objects.create_user(
            username=self.username,
            password='testpassword123',
            mobile=f'138{unique_suffix}'
        )
        print(f"Created test user: {self.username}")
        
        # Create a pet type
        self.pet_type_name = "Dog"
        self.pet_type = PetsType.objects.create(name=self.pet_type_name)
        print(f"Created pet type: {self.pet_type_name}")
        
        # Create pet information
        self.pet_name = f"Buddy_{unique_suffix}"
        self.pet = PetsInfo.objects.create(
            user=self.user,
            name=self.pet_name,
            intro="A friendly dog",
            area="Beijing",
            atype=self.pet_type,
            age=3,
            status=0
        )
        print(f"Pet created: {self.pet_name}")
    
    def test_pet_creation(self):
        """Test pet creation"""
        print("Execute test: test_pet_creation")
        self.assertEqual(self.pet.name, self.pet_name)
        self.assertEqual(self.pet.intro, "A friendly dog")
        self.assertEqual(self.pet.area, "Beijing")
        self.assertEqual(self.pet.age, 3)
        self.assertEqual(self.pet.atype.name, self.pet_type_name)
        self.assertEqual(self.pet.status, 0)
        print("Test passed: The pet creation function works normally")
    
    def test_pet_str_method(self):
        """Test pet string representation"""
        print("Execute test: test_pet_str_method")
        self.assertEqual(str(self.pet), self.pet_name)
        print("Test passed: The pet string representation method works normally")
    
    def test_pet_type_str_method(self):
        """Test pet type string representation"""
        print("Execute test: test_pet_type_str_method")
        self.assertEqual(str(self.pet_type), self.pet_type_name)
        print("Test passed: The pet type string representation method works normally")

if __name__ == '__main__':
    print("Start testing...")
    unittest.main(verbosity=2) 