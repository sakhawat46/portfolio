"""
Django settings for projects.
"""

from pathlib import Path
import os

try:
    import environ
except Exception:
    environ = None

BASE_DIR = Path(__file__).resolve().parent.parent

if environ:
    env = environ.Env(
        DEBUG=(bool, False),
    )
    environ.Env.read_env(BASE_DIR / ".env")
    get_env = env
else:
    class SimpleEnv:
        def __call__(self, key, default=None):
            value = os.getenv(key)
            if value is None:
                return default
            if isinstance(default, bool):
                return value.lower() in {"1", "true", "yes", "on"}
            return value

        def list(self, key, default=None):
            value = os.getenv(key)
            if value is None:
                return default or []
            return [item.strip() for item in value.split(",") if item.strip()]

        def db(self, key):
            import dj_database_url

            return dj_database_url.parse(os.getenv(key))

    get_env = SimpleEnv()

SECRET_KEY = get_env("SECRET_KEY", default="django-insecure-change-me")
DEBUG = get_env("DEBUG", default=True)
ALLOWED_HOSTS = get_env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "core",
    "portfolio",
    "blog",
    "contact",
]

try:
    import ckeditor  # noqa: F401

    INSTALLED_APPS.insert(7, "ckeditor")
except Exception:
    pass

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "projects.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "projects.wsgi.application"
ASGI_APPLICATION = "projects.asgi.application"

database_url = get_env("DATABASE_URL", default=None)
if database_url and environ:
    DATABASES = {"default": get_env.db("DATABASE_URL")}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
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
TIME_ZONE = get_env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 260,
    },
}
