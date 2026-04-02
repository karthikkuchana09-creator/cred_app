#!/bin/sh
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model();\
if not User.objects.filter(username='admin').exists():\
    User.objects.create_superuser('admin', 'admin@example.com', 'Admin@123')"
python manage.py runserver 0.0.0.0:8000
