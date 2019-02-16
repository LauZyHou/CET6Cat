"""
Django settings for CET6Cat project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
import datetime
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# -----------------------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 设置搜索app的路径
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "apps"))
sys.path.insert(0, os.path.join(BASE_DIR, "extra_apps"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/
# -----------------------------------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1llg(zkqrhys*((f75uyj5em=!%1poow9t_q3_1g(dca$khi)n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# 项目使用的Application
# -----------------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_jwt',
    'rest_framework.authtoken',  # 设置token
    'crispy_forms',
    'django_filters',
    'corsheaders',
    'reversion',
    'xadmin',
    'goods',
    # 'users.apps.UsersConfig',
    'users',
]

# 项目使用的中间件
# -----------------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS跨域
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # Django跨站请求保护
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 允许随意跨域
CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'CET6Cat.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CET6Cat.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
# -----------------------------------------------------------------------------------------
# 将默认的SQLite3数据库换成MySQL数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cet6cat',
        'USER': 'root',
        'PASSWORD': '3838438',
        'HOST': 'localhost',
        'PORT': '3306',
        # 第三方登录的库要求使用innodb,否则会migration出错?
        "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"}
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
# -----------------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
# -----------------------------------------------------------------------------------------

LANGUAGE_CODE = 'zh-hans'  # 语言改为中文

TIME_ZONE = 'Asia/Shanghai'  # 时区改为上海

USE_I18N = True

USE_L10N = True

USE_TZ = False  # 数据库存储使用时间,True时间会被存为UTC的时间

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
# -----------------------------------------------------------------------------------------
# 引用指针,在HTML文件中需要和这里对应.(这个名字和实际目录名无关)
STATIC_URL = '/static/'
# 建立一个全局变量元组,保存要引用的路径位置
STATICFILES_DIRS = (
    # 指出要引用的资源所在目录名字.(这个就是实际目录名,和引用指针名无关)
    os.path.join(BASE_DIR, 'static'),
)

# collectstatic收集到的目录
# -----------------------------------------------------------------------------------------
STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static')

# 设置图片访问的路径
# -----------------------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# 添加AUTH_USRE_MODEL 替换默认的user
# -----------------------------------------------------------------------------------------
AUTH_USER_MODEL = 'users.UserProfile'

# 所有与drf相关的设置写在这里面,其中的key可以到rest_framework模块下的setting里去找
# -----------------------------------------------------------------------------------------
REST_FRAMEWORK = {
    # 分页.注意设置分页后JSON的格式就变了
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 如果前端带错误的(如过期的)Token,那么在访问公共页面时还是会出认证错误
        # 所以不在这里配置全局的Token认证,而是改到views里配置
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # 改用JWT
        # JWT也和普通的Token一样,还是配置到具体要做验证的view里面去
    )
}

import datetime

JWT_AUTH = {
    # 设置过期时间为7天
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 请求时候HTTP头的Token前面的字符串,默认就是JWT.这里改掉让前端不知道服务器用的JWT
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
