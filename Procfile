release: python manage.py makemigrations && python manage.py migrate --noinput
web: gunicorn alvative_assessment.wsgi --timeout 300
