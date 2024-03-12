command = '/var/www/log_simplifier/env/bin/gunicorn'
python_path = '/var/www/log_simplifier/log_simplifier'
bind = '127.0.0.1:8001'
workers = 5
user = 'www'
raw_env = 'DJANGO_SETTINGS_MODULE=log_simplifier.settings'
