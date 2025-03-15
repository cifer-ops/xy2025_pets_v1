#!/usr/bin/env python
"""
一个非常简单的测试脚本，只测试UserProfile模型的最基本功能
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

class UserModelSimpleTest(unittest.TestCase):
    """用户模型的简单测试"""
    
    def setUp(self):
        """设置测试数据"""
        print("\n设置测试数据...")
        # 确保数据库表已创建
        from django.core.management import call_command
        call_command('migrate', verbosity=0)
        
        # 创建测试用户，使用随机后缀确保唯一性
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
        print(f"创建了测试用户: {self.username}")
    
    def test_user_creation(self):
        """测试用户创建"""
        print("执行测试: test_user_creation")
        self.assertEqual(self.user.username, self.username)
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.mobile, self.mobile)
        self.assertTrue(self.user.check_password('testpassword123'))
        print("测试通过: 用户创建功能正常工作")
    
    def test_user_str_method(self):
        """测试用户字符串表示"""
        print("执行测试: test_user_str_method")
        self.assertEqual(str(self.user), self.username)
        print("测试通过: 用户字符串表示方法正常工作")

if __name__ == '__main__':
    print("开始测试...")
    unittest.main(verbosity=2) 