#!/usr/bin/env python
"""A simple test script for pet collection features
Test collection model creation and basic query functions"""
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
from pets.models import PetsType, PetsInfo, Collect

class CollectTestCase(unittest.TestCase):
    """Collection function test"""
    
    def setUp(self):
        """Set up test data"""
        print("\nSet test data...")
        # Make sure the database table is created
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # Clear all data
        Collect.objects.all().delete()
        
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
    
    def tearDown(self):
        """Clean up test data"""
        print("Clean up test data...")
        # Clear all data
        Collect.objects.all().delete()
    
    def test_collect_creation(self):
        """Test Creation Collection"""
        print("Execute test: test_collect_creation")
        # Check the initial status
        self.assertEqual(Collect.objects.count(), 0, "There should be no favorite record in the initial state")
        
        # Create a collection
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        print(f"Created favorite record: ID={collect.id}")
        
        # Assert that collection was created successfully
        self.assertIsNotNone(collect.id)
        self.assertEqual(collect.user, self.user)
        self.assertEqual(collect.pet, self.pet)
        self.assertEqual(Collect.objects.count(), 1, "There should be only one favorite record")
        print("Test passed: Favorite creation function works normally")
    
    def test_collect_query(self):
        """Test query collection"""
        print("Execute test: test_collect_query")
        # Check the initial status
        self.assertEqual(Collect.objects.count(), 0, "There should be no favorite record in the initial state")
        
        # Create a collection
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        
        # Query Collection
        user_collects = Collect.objects.filter(user=self.user)
        self.assertEqual(user_collects.count(), 1)
        self.assertEqual(user_collects.first().pet, self.pet)
        
        pet_collects = Collect.objects.filter(pet=self.pet)
        self.assertEqual(pet_collects.count(), 1)
        self.assertEqual(pet_collects.first().user, self.user)
        print("Test passed: Favorite query function works normally")
    
    def test_collect_deletion(self):
        """Test Delete Collection"""
        print("Execute test: test_collect_deletion")
        # Check the initial status
        self.assertEqual(Collect.objects.count(), 0, "There should be no favorite record in the initial state")
        
        # Create a collection
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        
        # Check the existence of favorites
        self.assertEqual(Collect.objects.count(), 1, "There should be a favorite record")
        
        # Delete favorites
        collect.delete()
        
        # Check that collection has been deleted
        self.assertEqual(Collect.objects.count(), 0, "There should be no favorite record after deletion")
        print("Test passed: Favorites delete function works normally")

if __name__ == '__main__':
    print("Start testing...")
    unittest.main(verbosity=2) 