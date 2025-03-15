"""xy_pets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
import sys

# 简单的URL配置，用于测试
test_mode = 'test' in sys.argv

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path(r'', include(('pets.urls', 'pets'), namespace='pets')),
]

# 只在非测试模式下添加ckeditor URLs
if not test_mode:
    try:
        urlpatterns.append(re_path(r'^ckeditor/', include('ckeditor_uploader.urls')))
    except ImportError:
        pass  # ckeditor_uploader不可用，但这不影响测试

if settings.DEBUG:
    urlpatterns.append(re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}))
