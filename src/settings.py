# -*- coding: UTF-8 -*-

# You have to customize your properties files. Just make a copy from
# properties.py.template and change the parameters to adapt them to your needs.
import properties

DEBUG = getattr(properties, 'debug', True)
TEMPLATE_DEBUG = getattr(properties,'template_debug', True)

SITE_ROOT= getattr(properties, 'site_root', "http://localhost:8000/")

MANAGERS = getattr(properties, 'managers', ())

DATABASE_ENGINE = getattr(properties, 'database_engine', 'sqlite3')   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = getattr(properties, 'database_name', 'db.sqlite')     # Or path to database file if using sqlite3.
DATABASE_USER = getattr(properties, 'database_user', None)            # Not used with sqlite3.
DATABASE_PASSWORD = getattr(properties, 'database_password', '')      # Not used with sqlite3.
DATABASE_HOST = getattr(properties, 'database_host','')               # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = getattr(properties, 'database_port','')               # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be avilable on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = getattr(properties,'time_zone', 'Europe/Madrid')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = getattr(properties, 'language_code', 'en-en')

SITE_ID = getattr(properties, 'site_id', 1)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = getattr(properties,'use_i18n', True)
USE_L10N = getattr(properties,'use_l10n', True)
# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = getattr(properties, 'media_root', '.')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = getattr(properties, 'media_url','http://localhost:8000/media/')

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = getattr(properties, 'admin_media_prefix','/adm_media/')

# Make this unique, and don't share it with anybody.
SECRET_KEY = getattr(properties, 'secret_key','secret-key')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = getattr(properties, 'template_dirs', ('templates',))


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'south',
    'django_nose', #ha d'anar després de south
    'debug_toolbar',
    'motor',
    'recepcion',
    'captcha',
    'contacto',
    'faq',
)

# set cache adn session backend
CACHE_BACKEND=getattr(properties, 'cache_backend','dummy:///')
CACHE_MIDDLEWARE_KEY_PREFIX=getattr(properties, 'cache_prefix', 'motor')
CACHE_MIDDLEWARE_SECONDS=getattr(properties, 'cache_seconds', 5)
SESSION_BACKEND=getattr(properties, 'session_backend','django.contrib.sessions.backends.cache')

if DEBUG:
    SESSION_EXPIRE_AT_BROWSER_CLOSE=True

ugettext = lambda s:s
LANGUAGES = (
    ('en', ugettext('English')),
    ('es', ugettext('Spanish')),
    ('ca', ugettext('Catalan')),
)

TEMPLATE_CONTEXT_PROCESSORS=("django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request")

COPYRIGHT="apsl.net"

# NOSE_TESTS
TEST_RUNNER = 'django_nose.run_tests'

# Debug toolbar configuration
INTERNAL_IPS=('127.0.0.2',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

EMAIL_CONTACTO = getattr(properties, 'email_contacto', ['info@apsl.net',])
