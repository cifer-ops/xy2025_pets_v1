from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from .models import PetsType, PetsInfo, Collect, Adoption
import json
import os
import sys

# Set up the Django environment so that the test can run independently
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xy_pets.settings')
import django
django.setup()

class PetsModelTest(TestCase):
    """Pet model testing"""
    
    def setUp(self):
        """Set up test data"""
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
        self.pet_type = PetsType.objects.create(name='Dog')
        self.pet = PetsInfo.objects.create(
            user=self.user,
            name='Buddy',
            intro='A friendly dog',
            area='Beijing',
            atype=self.pet_type,
            age=3,
            status=0
        )
    
    def test_pet_creation(self):
        """Test pet creation"""
        self.assertEqual(self.pet.name, 'Buddy')
        self.assertEqual(self.pet.intro, 'A friendly dog')
        self.assertEqual(self.pet.area, 'Beijing')
        self.assertEqual(self.pet.age, 3)
        self.assertEqual(self.pet.atype.name, 'Dog')
        self.assertEqual(self.pet.status, 0)
    
    def test_pet_str_method(self):
        """Test pet string representation"""
        self.assertEqual(str(self.pet), 'Buddy')
    
    def test_pet_type_str_method(self):
        """Test pet type string representation"""
        self.assertEqual(str(self.pet_type), 'Dog')


class PetsViewTest(TestCase):
    """Pet View Test"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.list_url = reverse('pets')
        
        # Create a user
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
        
        # Create a pet type
        self.pet_type = PetsType.objects.create(name='Dog')
        self.pet_type2 = PetsType.objects.create(name='Cat')
        
        # Create pet information
        self.pet1 = PetsInfo.objects.create(
            user=self.user,
            name='Buddy',
            intro='A friendly dog',
            area='Beijing',
            atype=self.pet_type,
            age=3,
            status=0
        )
        
        self.pet2 = PetsInfo.objects.create(
            user=self.user,
            name='Kitty',
            intro='A cute cat',
            area='Shanghai',
            atype=self.pet_type2,
            age=2,
            status=0
        )
    
    def test_pets_list_view(self):
        """Test pet list page"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertContains(response, 'Kitty')
    
    def test_pet_detail_view(self):
        """Test pet details page"""
        detail_url = reverse('detail') + f'?wid={self.pet1.id}'
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertContains(response, 'A friendly dog')
    
    def test_filter_by_type(self):
        """Test filter by type"""
        filter_url = reverse('pets') + f'?t={self.pet_type.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertNotContains(response, 'Kitty')


class CollectTest(TestCase):
    """Collection function test"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create a user
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
        
        # Create pet types and pets
        self.pet_type = PetsType.objects.create(name='Dog')
        self.pet = PetsInfo.objects.create(
            user=self.user,
            name='Buddy',
            intro='A friendly dog',
            area='Beijing',
            atype=self.pet_type,
            age=3,
            status=0
        )
        
        # Log in to the user
        self.client.login(username='testuser', password='testpassword123')
    
    def test_collect_pet(self):
        """Test collection of pets"""
        # Check the initial status without collection
        self.assertEqual(Collect.objects.count(), 0)
        
        # Perform a favorite operation
        collect_url = reverse('collect')
        response = self.client.post(collect_url, {'wid': self.pet.id})
        
        # Check responses and databases
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Collect.objects.count(), 1)
        self.assertTrue(Collect.objects.filter(user=self.user, pet=self.pet).exists())
        
        # Check my favorite page
        my_collect_url = reverse('my_collect')
        response = self.client.get(my_collect_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')


class AdoptionTest(TestCase):
    """Adoption function test"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create a user
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
        
        # Create pet types and pets
        self.pet_type = PetsType.objects.create(name='Dog')
        self.pet = PetsInfo.objects.create(
            user=self.user,
            name='Buddy',
            intro='A friendly dog',
            area='Beijing',
            atype=self.pet_type,
            age=3,
            status=0
        )
        
        # Log in to the user
        self.client.login(username='testuser', password='testpassword123')
    
    def test_apply_adoption(self):
        """Test application for adoption"""
        # Check initial status without adoption application
        self.assertEqual(Adoption.objects.count(), 0)
        
        # Execute adoption application
        adopt_url = reverse('adopt')
        response = self.client.post(adopt_url, {'wid': self.pet.id})
        
        # Check responses and databases
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Adoption.objects.count(), 1)
        
        # Check my adoption page
        my_adoption_url = reverse('my_adoption')
        response = self.client.get(my_adoption_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')

if __name__ == '__main__':
    import unittest
    unittest.main()
