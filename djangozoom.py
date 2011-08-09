import logging 

DATABASES = {
    "default": {
        "ENGINE": "postgresql_psycopg2", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": "packaginator",          # Or path to database file if using sqlite3.
        "USER": "",              # Not used with sqlite3.
        "PASSWORD": "",                  # Not used with sqlite3.
        "HOST": "",             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                  # Set to empty string for default. Not used with sqlite3.
    }
}


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SERVE_MEDIA = DEBUG
#TEST_RUNNER = 'testrunner.OurTestRunner'

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s "%(message)s" in %(funcName)s() line %(lineno)d in %(pathname)s', 
        filename='main.log',
        filemode='a',
)

LOCAL_INSTALLED_APPS = []

ROOT_URLCONF = "packaginator.urls"

LAUNCHPAD_ACTIVE = False

# Analytics ID
URCHIN_ID = ""

# Email Settings
DEFAULT_FROM_EMAIL = 'Django Packages <djangopackages-noreply@djangopackages.com>'
EMAIL_SUBJECT_PREFIX = '[Django Packages] '

# Make this unique, and don't share it with anybody.
SECRET_KEY = "blarg-a-flarg"

# See http://celeryproject.org/docs/configuration.html#task-execution-settings
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
BROKER_BACKEND = "django"

LOCAL_INSTALLED_APPS = ('djkombu', )

ACCOUNT_OPEN_SIGNUP = False