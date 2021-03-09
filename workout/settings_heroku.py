from workout.settings import *

DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL')
        )
    }

DOMAIN = os.environ.get('DOMAIN', None)
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', None)
if HEROKU_APP_NAME and not DOMAIN:
    DOMAIN = '%s.herokuapp.com' % HEROKU_APP_NAME
elif not DOMAIN:
    DOMAIN = 'localhost:8000'
ALLOWED_HOSTS.append(DOMAIN)

MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
