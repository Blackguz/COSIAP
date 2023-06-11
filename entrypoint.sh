#!/bin/sh

python manage.py migrate
python manage.py loaddata convocatorias/fixtures/estatus_initial_data
exec "$@"
