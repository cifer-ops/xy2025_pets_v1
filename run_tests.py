#!/usr/bin/env python
"""
运行单元测试的脚本，使用简化的测试设置
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # 使用简化的测试设置
    os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'
    django.setup()
    
    # 运行测试
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # 准备测试参数
    test_args = sys.argv[1:] or ['accounts', 'pets']
    
    print(f"正在运行测试: {', '.join(test_args)}")
    failures = test_runner.run_tests(test_args)
    
    # 退出码 - 如果有失败的测试则返回非零值
    sys.exit(bool(failures)) 