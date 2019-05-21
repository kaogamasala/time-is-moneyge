"""
Django settings for time_is_moneyge project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com', 'timeismoneyge.herokuapp.com']

# django-crispy-forms 設定
CRISPY_TEMPLATE_PACK = 'bootstrap4'
#humanizeのintcomma桁数
NUMBER_GROUPING = 3
DURATION_INPUT_FORMATS = ['%H:%M:%S']
#placeholderの表示
BOOTSTRAP4 = { 'set_placeholder': True, } 

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tim_app', # Time_is_moneyge_app
    'accounts.apps.AccountsConfig', #ユーザー登録
    'django.contrib.humanize',
    'timedeltatemplatefilter', #templateでtimedeltaの表示をコントロールできる
    'bootstrap4',  # django-bootstrap4
    'crispy_forms', # django-crispy-forms
    'widget_tweaks', # widget_tweaks
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'time_is_moneyge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], #ベースディレクトリにテンプレートフォルダ
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

WSGI_APPLICATION = 'time_is_moneyge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}'''


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ja-JP'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"), #static
)

##################
# Authentication #
##################
LOGIN_REDIRECT_URL = 'https://timeismoneyge.herokuapp.com/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

# DEBUGがTrue場合の動作確認を想定した設定（パスワード再設定メール）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 拡張ユーザーモデルクラスを作成した場合定義する
AUTH_USER_MODEL = 'accounts.CustomUser'


# local_settings.py読み込み
try:
    from .local_settings import *
except ImportError:
    pass

# Debug=Falseの時だけ実行する設定
if not DEBUG:
    SECRET_KEY = os.environ['SECRET_KEY'] #追加
    import django_heroku
    django_heroku.settings(locals())

