[![Build Status](https://app.travis-ci.com/kpdvstu/PTLab2.svg?branch=master)](https://app.travis-ci.com/kpdvstu/PTLab2)
# Лабораторная 2 по дисциплине "Технологии программирования"

$env:PYTHONPATH = "ps_password"
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata products.yaml
python manage.py loaddata customers.yaml
python manage.py runserver

python manage.py test shop/tests/

create database django_db owner postgres;

pip install -r requirements.txt