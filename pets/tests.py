from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserProfile
from .models import PetsType, PetsInfo, Collect, Adoption
import json
import os
import sys

# 设置Django环境以便测试可以独立运行
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xy_pets.settings')
import django
django.setup()

class PetsModelTest(TestCase):
    """宠物模型测试"""
    
    def setUp(self):
        """设置测试数据"""
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
        """测试宠物创建"""
        self.assertEqual(self.pet.name, 'Buddy')
        self.assertEqual(self.pet.intro, 'A friendly dog')
        self.assertEqual(self.pet.area, 'Beijing')
        self.assertEqual(self.pet.age, 3)
        self.assertEqual(self.pet.atype.name, 'Dog')
        self.assertEqual(self.pet.status, 0)
    
    def test_pet_str_method(self):
        """测试宠物字符串表示"""
        self.assertEqual(str(self.pet), 'Buddy')
    
    def test_pet_type_str_method(self):
        """测试宠物类型字符串表示"""
        self.assertEqual(str(self.pet_type), 'Dog')


class PetsViewTest(TestCase):
    """宠物视图测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.client = Client()
        self.list_url = reverse('pets')
        
        # 创建用户
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
        
        # 创建宠物类型
        self.pet_type = PetsType.objects.create(name='Dog')
        self.pet_type2 = PetsType.objects.create(name='Cat')
        
        # 创建宠物信息
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
        """测试宠物列表页面"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertContains(response, 'Kitty')
    
    def test_pet_detail_view(self):
        """测试宠物详情页面"""
        detail_url = reverse('detail') + f'?wid={self.pet1.id}'
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertContains(response, 'A friendly dog')
    
    def test_filter_by_type(self):
        """测试按类型筛选"""
        filter_url = reverse('pets') + f'?t={self.pet_type.id}'
        response = self.client.get(filter_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')
        self.assertNotContains(response, 'Kitty')


class CollectTest(TestCase):
    """收藏功能测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.client = Client()
        
        # 创建用户
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
        
        # 创建宠物类型和宠物
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
        
        # 登录用户
        self.client.login(username='testuser', password='testpassword123')
    
    def test_collect_pet(self):
        """测试收藏宠物"""
        # 检查初始状态无收藏
        self.assertEqual(Collect.objects.count(), 0)
        
        # 执行收藏操作
        collect_url = reverse('collect')
        response = self.client.post(collect_url, {'wid': self.pet.id})
        
        # 检查响应和数据库
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Collect.objects.count(), 1)
        self.assertTrue(Collect.objects.filter(user=self.user, pet=self.pet).exists())
        
        # 检查我的收藏页面
        my_collect_url = reverse('my_collect')
        response = self.client.get(my_collect_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')


class AdoptionTest(TestCase):
    """领养功能测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.client = Client()
        
        # 创建用户
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
        
        # 创建宠物类型和宠物
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
        
        # 登录用户
        self.client.login(username='testuser', password='testpassword123')
    
    def test_apply_adoption(self):
        """测试申请领养"""
        # 检查初始状态无领养申请
        self.assertEqual(Adoption.objects.count(), 0)
        
        # 执行领养申请
        adopt_url = reverse('adopt')
        response = self.client.post(adopt_url, {'wid': self.pet.id})
        
        # 检查响应和数据库
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Adoption.objects.count(), 1)
        
        # 检查我的领养页面
        my_adoption_url = reverse('my_adoption')
        response = self.client.get(my_adoption_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Buddy')

if __name__ == '__main__':
    import unittest
    unittest.main()
