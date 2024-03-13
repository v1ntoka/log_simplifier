#!/bin/bash
source /var/www/log_simplifier/env/bin/activate
exec gunicorn -c "/var/www/log_simplifier/log_simplifier/gunicorn_config.py" log_simplifier.wsgi