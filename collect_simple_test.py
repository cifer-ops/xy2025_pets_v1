#!/usr/bin/env python
"""
一个针对宠物收藏功能的简单测试脚本
测试收藏模型的创建和基本查询功能
"""
import sys
import os
import django
from django.conf import settings
import unittest
import uuid

# 配置Django环境
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# 极简配置，只包含必要的设置
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

print("配置Django环境...")
# 应用配置
settings.configure(**config)
django.setup()

# 导入要测试的模型
from accounts.models import UserProfile
from pets.models import PetsType, PetsInfo, Collect

class CollectTestCase(unittest.TestCase):
    """收藏功能测试"""
    
    def setUp(self):
        """设置测试数据"""
        print("\n设置测试数据...")
        # 确保数据库表已创建
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # 清空所有数据
        Collect.objects.all().delete()
        
        # 创建唯一的测试用户
        unique_suffix = str(uuid.uuid4())[:8]
        self.username = f'testuser_{unique_suffix}'
        self.user = UserProfile.objects.create_user(
            username=self.username,
            password='testpassword123',
            mobile=f'138{unique_suffix}'
        )
        print(f"创建了测试用户: {self.username}")
        
        # 创建宠物类型
        self.pet_type_name = "Dog"
        self.pet_type = PetsType.objects.create(name=self.pet_type_name)
        
        # 创建宠物信息
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
        print(f"创建了宠物: {self.pet_name}")
    
    def tearDown(self):
        """清理测试数据"""
        print("清理测试数据...")
        # 清空所有数据
        Collect.objects.all().delete()
    
    def test_collect_creation(self):
        """测试创建收藏"""
        print("执行测试: test_collect_creation")
        # 检查初始状态
        self.assertEqual(Collect.objects.count(), 0, "初始状态应该没有收藏记录")
        
        # 创建收藏
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        print(f"创建了收藏记录: ID={collect.id}")
        
        # 断言收藏创建成功
        self.assertIsNotNone(collect.id)
        self.assertEqual(collect.user, self.user)
        self.assertEqual(collect.pet, self.pet)
        self.assertEqual(Collect.objects.count(), 1, "应该只有一条收藏记录")
        print("测试通过: 收藏创建功能正常工作")
    
    def test_collect_query(self):
        """测试查询收藏"""
        print("执行测试: test_collect_query")
        # 检查初始状态
        self.assertEqual(Collect.objects.count(), 0, "初始状态应该没有收藏记录")
        
        # 创建收藏
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        
        # 查询收藏
        user_collects = Collect.objects.filter(user=self.user)
        self.assertEqual(user_collects.count(), 1)
        self.assertEqual(user_collects.first().pet, self.pet)
        
        pet_collects = Collect.objects.filter(pet=self.pet)
        self.assertEqual(pet_collects.count(), 1)
        self.assertEqual(pet_collects.first().user, self.user)
        print("测试通过: 收藏查询功能正常工作")
    
    def test_collect_deletion(self):
        """测试删除收藏"""
        print("执行测试: test_collect_deletion")
        # 检查初始状态
        self.assertEqual(Collect.objects.count(), 0, "初始状态应该没有收藏记录")
        
        # 创建收藏
        collect = Collect.objects.create(
            user=self.user,
            pet=self.pet
        )
        
        # 检查收藏存在
        self.assertEqual(Collect.objects.count(), 1, "应该有一条收藏记录")
        
        # 删除收藏
        collect.delete()
        
        # 检查收藏已删除
        self.assertEqual(Collect.objects.count(), 0, "删除后应该没有收藏记录")
        print("测试通过: 收藏删除功能正常工作")

if __name__ == '__main__':
    print("开始测试...")
    unittest.main(verbosity=2) 