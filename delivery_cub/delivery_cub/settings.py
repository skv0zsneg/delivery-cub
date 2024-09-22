from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from . import __project_name__, __version__

load_dotenv("../../")

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = getenv("SECRET_KEY", False)
DEBUG = getenv("DEBUG", False)

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "app.cart",
    "app.order",
    "app.restaurant",
    "app.user",

    "rest_framework",
    "django_filters",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    "TITLE": f"{__project_name__} API",
    "VERSION": f"{__version__}",
    "CONTACT": {
        "name": "GitHub - skv0zsneg",
        "url": "https://github.com/skv0zsneg",
    },
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "filter": True,
    },
    "COMPONENT_SPLIT_REQUEST": True,
    "SERVE_PERMISSIONS": ['rest_framework.permissions.IsAuthenticatedOrReadOnly'],
}

ROOT_URLCONF = "delivery_cub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "delivery_cub.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("DB_NAME"),
        "USER": getenv("DB_USER"),
        "PASSWORD": getenv("DB_PASSWORD"),
        "HOST": getenv("DB_HOST"),
        "PORT": getenv("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = Path(BASE_DIR, "staticfiles")
LOGIN_REDIRECT_URL = "api/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"
DJANGO_ADMIN_NAME = getenv("DJANGO_ADMIN_NAME")
DJANGO_ADMIN_PASSWORD = getenv("DJANGO_ADMIN_PASSWORD")
DJANGO_ADMIN_EMAIL = getenv("DJANGO_ADMIN_EMAIL")
