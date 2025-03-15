from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import UserProfile
from .forms import LoginForm, RegisterForm
import os
import sys

# 设置Django环境以便测试可以独立运行
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xy_pets.settings')
import django
django.setup()

# Create your tests here.

class UserModelTest(TestCase):
    """用户模型测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.user = UserProfile.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123',
            mobile='13800138000'
        )
    
    def test_user_creation(self):
        """测试用户创建"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.mobile, '13800138000')
        self.assertTrue(self.user.check_password('testpassword123'))
    
    def test_user_str_method(self):
        """测试用户字符串表示"""
        self.assertEqual(str(self.user), 'testuser')


class LoginViewTest(TestCase):
    """登录视图测试"""
    
    def setUp(self):
        """设置测试数据"""
        self.client = Client()
        self.login_url = reverse('login')
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpassword123',
            mobile='13800138000'
        )
    
    def test_login_view_get(self):
        """测试GET请求登录页面"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_view_post_success(self):
        """测试成功登录"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # 重定向状态码
        
    def test_login_view_post_invalid(self):
        """测试无效登录"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "用户名或密码错误")


class RegisterFormTest(TestCase):
    """注册表单测试"""
    
    def test_valid_form(self):
        """测试有效的注册表单"""
        form_data = {
            'username': 'newuser',
            'password': 'newpassword123',
            'password2': 'newpassword123',
            'mobile': '13900139000'
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_password_mismatch(self):
        """测试密码不匹配"""
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
