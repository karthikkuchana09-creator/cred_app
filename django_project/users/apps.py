from django.apps import AppConfig


class UsersConfig(AppConfig):# This class defines the configuration for the 'users' app in a Django project.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users' # This is the name of the app, which should match the name of the directory containing this file.
