import ast
import os
import random
import sys
from datetime import timedelta
from pathlib import Path
from corsheaders.defaults import default_headers
from dotenv import load_dotenv

load_dotenv(".env")

config = os.environ
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root = lambda *x: BASE_DIR.joinpath(*x)
sys.path.insert(0, str(root("apps")))



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get("SECRET_KEY", "default secret for the hub")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(config.get("DEBUG", "False"))
IS_DEBUG_TOOL_ACTIVE = ast.literal_eval(
    config.get("IS_DEBUG_TOOL_ACTIVE", "False")
)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_extensions",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
]

PROJECT_APPS = [
    "hub"
]

INSTALLED_APPS += PROJECT_APPS

# ES config

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "backend.urls"

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

WSGI_APPLICATION = "backend.wsgi.application"

if IS_DEBUG_TOOL_ACTIVE:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = ["127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# DATABASE_ROUTERS = ["utils.dbrouter.PrimaryReplicaRouter"]
# DATABASES = {
#     "default": {
#         "ENGINE": config["MASTER_DB_ENGINE"],
#         "NAME": config["MASTER_DB_NAME"],
#         "USER": config["MASTER_DB_USER"],
#         "PASSWORD": config["MASTER_DB_PASSWORD"],
#         # an url IP Address that your DB is hosted
#         "HOST": config["MASTER_DB_HOST"],
#         "PORT": config["MASTER_DB_PORT"],
#     },
#     "slave": {
#         "ENGINE": config["SLAVE_DB_ENGINE"],
#         "NAME": config.get("SLAVE_DB_NAME"),
#         "USER": config.get("SLAVE_DB_USER"),
#         "PASSWORD": config.get("SLAVE_DB_PASSWORD"),
#         # Or an IP Address that your DB is hosted on
#         "HOST": config.get("SLAVE_DB_HOST"),
#         "PORT": config.get("SLAVE_DB_PORT"),
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
# django variable
LANGUAGE_CODE = "en-us"
USE_TZ = True
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_L10N = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
MEDIA_URL = "/media/"
SITE_ID = 1
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Cors Settings
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    *default_headers,
    "x-api-key",
    "Set-Cookie",
    "Device-Type",
]
CORS_EXPOSE_HEADERS = ["WWW-Authenticate", "Set-Cookie"]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
JWT_COOKIE_NAME = config.get("JWT_COOKIE_NAME", "refresh_token")
JWT_COOKIE_SAMESITE = config.get("JWT_COOKIE_SAMESITE", "Lax")
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_REDIRECT_URL = "home/"
LOGOUT_REDIRECT_URL = "home/"

WEB_API_KEY = config.get("X_API_KEY", "3283nnq22")
API_URL = config.get("API_URL", "")

LOGIN_URL = "/login/"

# Frontend Urls
FRONTEND_URL = config.get("FRONTEND_URL", "https://www.xtage.com")
SESSION_DOMAIN_NAME = config.get("SESSION_DOMAIN_NAME", ".xtage.com")

# Redis database for caching and background
MAX_CACHE_TIMEOUT = 864000 * 5 * random.choice(range(1, 20))
REDIS_HOST = "redis://" + config.get("REDIS_HOST", "localhost")
REDIS_DB = config.get("REDIS_DB", "10")
HTTP_X_API_KEY = config["X_API_KEY"]
REDIS_CACHE_PREFIX = "campaign_cache"
REDIS_MAX_TIMEOUT = 24 * 60 * 60 * 365  # Maximum one year of caching
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_HOST + "/" + REDIS_DB,
        "DB": REDIS_DB,
        "TIMEOUT": 60 * 60 * 24,  # 1 day
        "KEY_PREFIX": SESSION_DOMAIN_NAME,
    }
}
# Aws configuration



# monitoring tools


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s [%(asctime)s] %(module)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "custom": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
