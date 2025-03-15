#!/usr/bin/env python
"""
一个非常简单的测试脚本，只测试PetsInfo和PetsType模型的最基本功能
不依赖Django测试框架，实现最小的测试依赖
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
from pets.models import PetsType, PetsInfo

class PetsModelSimpleTest(unittest.TestCase):
    """宠物模型的简单测试"""
    
    def setUp(self):
        """设置测试数据"""
        print("\n设置测试数据...")
        # 确保数据库表已创建
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
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
        print(f"创建了宠物类型: {self.pet_type_name}")
        
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
    
    def test_pet_creation(self):
        """测试宠物创建"""
        print("执行测试: test_pet_creation")
        self.assertEqual(self.pet.name, self.pet_name)
        self.assertEqual(self.pet.intro, "A friendly dog")
        self.assertEqual(self.pet.area, "Beijing")
        self.assertEqual(self.pet.age, 3)
        self.assertEqual(self.pet.atype.name, self.pet_type_name)
        self.assertEqual(self.pet.status, 0)
        print("测试通过: 宠物创建功能正常工作")
    
    def test_pet_str_method(self):
        """测试宠物字符串表示"""
        print("执行测试: test_pet_str_method")
        self.assertEqual(str(self.pet), self.pet_name)
        print("测试通过: 宠物字符串表示方法正常工作")
    
    def test_pet_type_str_method(self):
        """测试宠物类型字符串表示"""
        print("执行测试: test_pet_type_str_method")
        self.assertEqual(str(self.pet_type), self.pet_type_name)
        print("测试通过: 宠物类型字符串表示方法正常工作")

if __name__ == '__main__':
    print("开始测试...")
    unittest.main(verbosity=2) 