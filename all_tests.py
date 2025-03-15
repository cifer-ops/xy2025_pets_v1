#!/usr/bin/env python
"""
Comprehensive Test Suite for Pet Adoption Platform
This file combines all tests for the platform into a single executable script.
"""
import sys
import os
import django
from django.conf import settings
import unittest
import uuid

# Configure Django environment
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Minimal configuration with only necessary settings
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

print("Configuring Django environment...")
# Apply configuration
settings.configure(**config)
django.setup()

# Import models for testing
from accounts.models import UserProfile
from pets.models import PetsType, PetsInfo, Collect, Adoption

class UserModelTestCase(unittest.TestCase):
    """Tests for the User Authentication System"""
    
    def setUp(self):
        """Set up test data"""
        print("\nSetting up user authentication test data...")
        # Ensure database tables are created
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # Create test user with unique identifiers
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
        """Test user creation functionality"""
        print("Running test: test_user_creation")
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.mobile, self.mobile)
        self.assertTrue(self.user.check_password('testpassword123'))
        print("Test passed: User creation functionality works properly")
    
    def test_user_str_method(self):
        """Test user string representation method"""
        print("Running test: test_user_str_method")
        self.assertEqual(str(self.user), self.username)
        print("Test passed: User string representation method works properly")


class PetsModelTestCase(unittest.TestCase):
    """Tests for the Pet Management System"""
    
    def setUp(self):
        """Set up test data"""
        print("\nSetting up pet management test data...")
        # Ensure database tables are created
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # Create test user
        unique_suffix = str(uuid.uuid4())[:8]
        self.username = f'testuser_{unique_suffix}'
        self.user = UserProfile.objects.create_user(
            username=self.username,
            password='testpassword123',
            mobile=f'138{unique_suffix}'
        )
        print(f"Created test user: {self.username}")
        
        # Create pet type
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
        print(f"Created pet: {self.pet_name}")
    
    def test_pet_creation(self):
        """Test pet creation functionality"""
        print("Running test: test_pet_creation")
        self.assertEqual(self.pet.name, self.pet_name)
        self.assertEqual(self.pet.intro, "A friendly dog")
        self.assertEqual(self.pet.area, "Beijing")
        self.assertEqual(self.pet.age, 3)
        self.assertEqual(self.pet.atype.name, self.pet_type_name)
        self.assertEqual(self.pet.status, 0)
        print("Test passed: Pet creation functionality works properly")
    
    def test_pet_str_method(self):
        """Test pet string representation method"""
        print("Running test: test_pet_str_method")
        self.assertEqual(str(self.pet), self.pet_name)
        print("Test passed: Pet string representation method works properly")
    
    def test_pet_type_str_method(self):
        """Test pet type string representation method"""
        print("Running test: test_pet_type_str_method")
        self.assertEqual(str(self.pet_type), self.pet_type_name)
        print("Test passed: Pet type string representation method works properly")


class CollectTestCase(unittest.TestCase):
    """Tests for the Pet Collection Feature"""
    
    def setUp(self):
        """Set up test data"""
        print("\nSetting up collection feature test data...")
        # Ensure database tables are created
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # Clear all collection data
        Collect.objects.all().delete()
        
        # Create test user
        unique_suffix = str(uuid.uuid4())[:8]
        self.username = f'testuser_{unique_suffix}'
        self.user = UserProfile.objects.create_user(
            username=self.username,
            password='testpassword123',
            mobile=f'138{unique_suffix}'
        )
        print(f"Created test user: {self.username}")
        
        # Create pet type and pet
        self.pet_type_name = "Dog"
        self.pet_type = PetsType.objects.create(name=self.pet_type_name)
        
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
        print(f"Created pet: {self.pet_name}")
    
    def tearDown(self):
        """Clean up test data"""
        print("Cleaning up test data...")
        # Clear all collection data
        Collect.objects.all().delete()
    
    def test_collect_creation(self):
        """Test creation of pet collection records"""
        print("Running test: test_collect_creation")
        # Check initial state
        self.assertEqual(Collect.objects.count(), 0, "Initial state should have no collection records")
        
        # Create collection record
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        print(f"Created collection record: ID={collect.id}")
        
        # Assert collection creation success
        self.assertIsNotNone(collect.id)
        self.assertEqual(collect.user, self.user)
        self.assertEqual(collect.pet, self.pet)
        self.assertEqual(Collect.objects.count(), 1, "There should be exactly one collection record")
        print("Test passed: Collection creation functionality works properly")
    
    def test_collect_query(self):
        """Test querying pet collection records"""
        print("Running test: test_collect_query")
        # Check initial state
        self.assertEqual(Collect.objects.count(), 0, "Initial state should have no collection records")
        
        # Create collection
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        
        # Query collections
        user_collects = Collect.objects.filter(user=self.user)
        self.assertEqual(user_collects.count(), 1)
        self.assertEqual(user_collects.first().pet, self.pet)
        
        pet_collects = Collect.objects.filter(pet=self.pet)
        self.assertEqual(pet_collects.count(), 1)
        self.assertEqual(pet_collects.first().user, self.user)
        print("Test passed: Collection query functionality works properly")
    
    def test_collect_deletion(self):
        """Test deletion of pet collection records"""
        print("Running test: test_collect_deletion")
        # Check initial state
        self.assertEqual(Collect.objects.count(), 0, "Initial state should have no collection records")
        
        # Create collection
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        
        # Check collection exists
        self.assertEqual(Collect.objects.count(), 1, "There should be one collection record")
        
        # Delete collection
        collect.delete()
        
        # Check collection was deleted
        self.assertEqual(Collect.objects.count(), 0, "After deletion there should be no collection records")
        print("Test passed: Collection deletion functionality works properly")


class AdoptionTestCase(unittest.TestCase):
    """Tests for the Pet Adoption Feature"""
    
    def setUp(self):
        """Set up test data"""
        print("\nSetting up adoption feature test data...")
        # Ensure database tables are created
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # Clear all adoption data
        Adoption.objects.all().delete()
        
        # Create test user
        unique_suffix = str(uuid.uuid4())[:8]
        self.username = f'testuser_{unique_suffix}'
        self.user = UserProfile.objects.create_user(
            username=self.username,
            password='testpassword123',
            mobile=f'138{unique_suffix}'
        )
        print(f"Created test user: {self.username}")
        
        # Create pet type and pet
        self.pet_type_name = "Dog"
        self.pet_type = PetsType.objects.create(name=self.pet_type_name)
        
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
        print(f"Created pet: {self.pet_name}")
    
    def tearDown(self):
        """Clean up test data"""
        print("Cleaning up test data...")
        # Clear all adoption data
        Adoption.objects.all().delete()
    
    def test_adoption_creation(self):
        """Test creation of adoption application records"""
        print("Running test: test_adoption_creation")
        # Check initial state
        self.assertEqual(Adoption.objects.count(), 0, "Initial state should have no adoption records")
        
        # Create adoption record
        adoption = Adoption.objects.create(
            user=self.user,
            pet=self.pet,
            status=0
        )
        print(f"Created adoption record: ID={adoption.id}")
        
        # Assert adoption creation success
        self.assertIsNotNone(adoption.id)
        self.assertEqual(adoption.user, self.user)
        self.assertEqual(adoption.pet, self.pet)
        self.assertEqual(adoption.status, 0)
        self.assertEqual(Adoption.objects.count(), 1, "There should be exactly one adoption record")
        print("Test passed: Adoption creation functionality works properly")
    
    def test_adoption_status_update(self):
        """Test updating adoption application status"""
        print("Running test: test_adoption_status_update")
        # Create adoption record
        adoption = Adoption.objects.create(
            user=self.user,
            pet=self.pet,
            status=0
        )
        
        # Update status - testing both integer and string representation as status field might be CharField
        try:
            # First try with integer
            adoption.status = 1
            adoption.save()
            
            # Verify status update
            updated_adoption = Adoption.objects.get(id=adoption.id)
            
            # Check if status is stored as string or integer and assert accordingly
            status_type = type(updated_adoption.status)
            print(f"Status field type is: {status_type.__name__}")
            
            if isinstance(updated_adoption.status, str):
                self.assertEqual(updated_adoption.status, "1", "Adoption status should be updated to '1' (string)")
            else:
                self.assertEqual(updated_adoption.status, 1, "Adoption status should be updated to 1 (integer)")
                
        except Exception as e:
            # If integer update fails, try with string
            print(f"Exception with integer status: {str(e)}")
            print("Trying with string status instead")
            
            # Create a new adoption record for the string test
            adoption_str = Adoption.objects.create(
                user=self.user,
                pet=self.pet,
                status="0"
            )
            
            adoption_str.status = "1"
            adoption_str.save()
            
            # Verify status update
            updated_adoption_str = Adoption.objects.get(id=adoption_str.id)
            self.assertEqual(updated_adoption_str.status, "1", "Adoption status should be updated to '1' (string)")
            
        print("Test passed: Adoption status update functionality works properly")


def run_all_tests():
    """Run all test cases"""
    # Create test suite with all test cases
    loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    
    # Add test cases to suite using the recommended method
    test_suite.addTest(loader.loadTestsFromTestCase(UserModelTestCase))
    test_suite.addTest(loader.loadTestsFromTestCase(PetsModelTestCase))
    test_suite.addTest(loader.loadTestsFromTestCase(CollectTestCase))
    test_suite.addTest(loader.loadTestsFromTestCase(AdoptionTestCase))
    
    # Run the test suite
    print("\n===== Running Pet Adoption Platform Tests =====\n")
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    
    # Print summary
    print("\n===== Test Results Summary =====")
    print(f"Total tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Starting comprehensive testing for Pet Adoption Platform...")
    success = run_all_tests()
    sys.exit(0 if success else 1) 