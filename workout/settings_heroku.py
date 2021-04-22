from workout.settings import *

DOMAIN = os.environ.get('DOMAIN', None)
HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', None)
if HEROKU_APP_NAME and not DOMAIN:
    DOMAIN = '%s.herokuapp.com' % HEROKU_APP_NAME
elif not DOMAIN:
    DOMAIN = 'localhost:8000'
ALLOWED_HOSTS.append(DOMAIN)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME', None),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY', None),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET', None),
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
EMAIL_PORT = 587
EMAIL_USE_TLS = True

ADMINS = [('Admin', 'noreply.workout@gmail.com')]
ADMIN_EMAIL = 'Workout <%s>' % 'noreply.workout@gmail.com'

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'admin_email': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'workout.log.WorkoutDevEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'level': 'ERROR',
            'handlers': ['admin_email'],
        },
    },
}
