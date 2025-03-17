from .settings import *

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['134.209.40.24', 'localhost']

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xy_pets_db',
        'USER': 'root',
        'PASSWORD': '020117Xyz',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# HTTPS settings
SECURE_SSL_REDIRECT = False  # 设置为True启用HTTPS重定向
SESSION_COOKIE_SECURE = False  # 设置为True时，Cookie只通过HTTPS发送
CSRF_COOKIE_SECURE = False  # 设置为True时，CSRF Cookie只通过HTTPS发送
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True 