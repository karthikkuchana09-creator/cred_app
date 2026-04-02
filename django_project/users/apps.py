from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users' # This is the name of the app, which should match the name of the directory containing this file.
