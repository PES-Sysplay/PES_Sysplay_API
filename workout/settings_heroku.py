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

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER', '')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', '')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN', '')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', '')
EMAIL_USE_TLS = True

ADMINS = [('Arnau', 'arnau.casas@estudiantat.upc.edu')]
ADMINS_EMAIL = 'Workout <arnau.casas@estudiantat.upc.edu>'
