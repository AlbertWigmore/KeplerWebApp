#!/bin/bash
set -e

pep8 --exclude="*migrations*" --ignore=E402 .
python manage.py makemigrations
python manage.py migrate
