from pathlib import Path
from datetime import timedelta
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_KEY", 'django-insecure-x-3++)n1ouk(j9k%r(-h@uk%@*qwol5e0#9wo&we_$+eoa@8=i')

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = ['https://*.localhost:8002']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_nose',
    'django_prometheus',
    'users',
    # 'core',
    'sales',
    'stock',
    'reports'
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'pharm_backend.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

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

WSGI_APPLICATION = 'pharm_backend.wsgi.application'

AUTH_USER_MODEL = "users.CustomUser"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "secret",
        "HOST": "localhost",
        # "HOST": "postgres",
        "PORT": "5432",
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'AUTH_HEADER_TYPES': ('Bearer',),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    }
SESSION_COOKIE_SECURE = False

SESSION_COOKIE_HTTPONLY = True 

LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : False,

    'formatters' : {
        'main_formatter' : {
            'format' : "{asctime} - {levelname} - {module} - {message}",
            'style' : '{',
        },
    },

    'handlers' : {
        'console': {
            'class' : 'logging.StreamHandler',
            'formatter' : 'main_formatter',
        },
        'file': {
            'class' : 'logging.FileHandler',
            'filename' : 'log.txt',
            'formatter' : 'main_formatter',
        },
    },

    'loggers': {
        'main': {
            'handlers': ['file', 'console'],
            'propagate': True,
            'level': 'INFO',
        }
    }
}

