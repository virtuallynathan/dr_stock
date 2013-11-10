#!/bin/bash

python manage.py flush
echo "drop schema public cascade; create schema public;" | sudo -u postgres psql finance
python manage.py syncdb

