"""
Django settings for substantive project.

Generated by 'django-admin startproject' using Django 2.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from substantive.aws.conf import *
import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '(ssx)+*u-wqmn+64@byd!tv)(lf^lzn0mn4@k%h29qzxs#uvaq')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
import dj_database_url

ALLOWED_HOSTS = ['yellow919.herokuapp.com', '.theshrota.com']
APPEND_SLASH=False

FILE_UPLOAD_HANDLERS = ("django_excel.ExcelMemoryFileUploadHandler",
                        "django_excel.TemporaryExcelFileUploadHandler")



# Application definition
SITE_ID = 1


INSTALLED_APPS = [
 'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django_comments',
    'mptt',
    'tagging',
    'import_export',
    # 'testing',
    'crispy_forms',
    'widget_tweaks',
    # "djstripe",
    # "stripe",
    # "zinnia",
    'bootstrapform',
    # 'survey',
    'procedures',
    'compressor',
    'django_tables2',

 
    

]
COMPRESS_ENABLED = True



MIDDLEWARE = [
 'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.security.SecurityMiddleware',
    
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'substantive.urls'

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
                'django.template.context_processors.i18n',
                'zinnia.context_processors.version',
            ],
        },
    },
]

WSGI_APPLICATION = 'substantive.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)
# DATABASES['default']['CONN_MAX_AGE'] = 500

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
]



STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")


# AUTH_USER_MODEL = 'testing.User'


# LOGIN_URL = 'login'

# LOGOUT_URL = 'logout'

# LOGIN_REDIRECT_URL = 'home'

# LOGOUT_REDIRECT_URL = 'home'

# Messages built-in framework

# MESSAGE_TAGS = {
#     messages.DEBUG: 'alert-secondary',
#     messages.INFO: 'alert-info',
#     messages.SUCCESS: 'alert-success',
#     messages.WARNING: 'alert-warning',
#     messages.ERROR: 'alert-danger',
# }


# Third party apps configuration

CRISPY_TEMPLATE_PACK = 'bootstrap4'


# BRAINTREE_PRODUCTION = False  # We'll need this later to switch between the sandbox and live account
# BRAINTREE_MERCHANT_ID = 'dwgqv3p26z3dmgrt'
# BRAINTREE_PUBLIC_KEY = 'vrjhcwszf4srv5y2'
# BRAINTREE_PRIVATE_KEY = '1061a68ca94aa919362fa3ad487d4109'

if DEBUG:
    STRIPE_PUBLISHABLE_KEY = 'pk_test_JUQ0vH7xhAanm5fHrBVUTN33'
    STRIPE_SECRET_KEY = 'sk_test_abo093CcGpqup3enkiscI3wq'

else:
    STRIPE_PUBLISHABLE_KEY = "pk_test_JUQ0vH7xhAanm5fHrBVUTN33"
    STRIPE_SECRET_KEY = "sk_test_abo093CcGpqup3enkiscI3wq"


STRIPE_LIVE_PUBLIC_KEY = os.environ.get("STRIPE_LIVE_PUBLIC_KEY", "pk_test_JUQ0vH7xhAanm5fHrBVUTN33")
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "sk_test_abo093CcGpqup3enkiscI3wq")
STRIPE_TEST_PUBLIC_KEY = os.environ.get("STRIPE_TEST_PUBLIC_KEY", "pk_test_JUQ0vH7xhAanm5fHrBVUTN33")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_abo093CcGpqup3enkiscI3wq")
STRIPE_LIVE_MODE = False  # Change to True in production



CORS_REPLACE_HTTPS_REFERER      = True
HOST_SCHEME                     = "https://"
SECURE_PROXY_SSL_HEADER         = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT             = True
SESSION_COOKIE_SECURE           = True
CSRF_COOKIE_SECURE              = True
SECURE_HSTS_INCLUDE_SUBDOMAINS  = True
SECURE_HSTS_SECONDS             = 1000000
SECURE_FRAME_DENY               = True
