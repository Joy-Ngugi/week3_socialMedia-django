"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
import dj_database_url




print(os.environ.get('CLOUDINARY_URL'))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q&%-8*0_2bcb4lz1+tzxm*5(k_ph9jy#6_@w%z67b%h1w=g$(u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['week3-socialmedia-django-1.onrender.com','week3-socialmedia-django-2tc5.onrender.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'myapp',
    'cloudinary',
    
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

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# if os.environ.get('DATABASE_URL'):
#     DATABASES = {
#         'default': dj_database_url.parse(
#             "postgresql://test_blog_9wtd_user:AFQPO00LyhMWof0oi0q1YGmniGanQHDo@dpg-ctucoojtq21c73bhbd50-a.oregon-postgres.render.com/test_blog_9wtd"
#         )
        
#     }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': 'media_db',
#             'USER': 'media_user',
#             'PASSWORD': 'joyjoy',
#             'HOST': 'localhost',
#             'PORT': '5432',
#             'OPTIONS': {
#             'options': '-c search_path=public'
#             }
#         }
#     }

# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': 'media_db',
#             'USER': 'media_user',
#             'PASSWORD': 'joyjoy',
#             'HOST': 'localhost',
#             'PORT': '5432',
#             'OPTIONS': {
#             'options': '-c search_path=public'
#             }
#         }
#     }

DATABASES = {
        'default': dj_database_url.parse(
            "postgresql://vacation_findet_user:QiRIo86lTQyYQsRP67Jx4q1Lanwgl9Zl@dpg-cul0imq3esus73b1olpg-a.oregon-postgres.render.com/vacation_findet"
        )
        
    }

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static",]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/' # Redirect to home after login
LOGOUT_REDIRECT_URL ='/' # Redirect to home after logout
LOGIN_URL ='/accounts/login/'

# CLOUDINARY_STORAGE = {
#     'CLOUD_NAME': 'die2ahtwv',
#     'API_KEY': '549986534211541',
#     'API_SECRET': 'HhEKvblKPlBc1Hxe2Vuvo_nE2OU',
# }

cloudinary.config(
    cloud_name="die2ahtwv",
    api_key="284863194573627",
    api_secret="EeUhxjGf53JfSlDlWwzfIJPyfzk"
)


CLOUDINARY_URL = 'cloudinary://549986534211541:HhEKvblKPlBc1Hxe2Vuvo_nE2OU@die2ahtwv'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"