#!/bin/bash
if [ ! -e ./csv/data.done ]
then
    echo "First launch, import..."
    python manage.py database migrate
    python manage.py database upgrade
    python manage.py import_csv -c ./csv/data.csv
    cp ./csv/data.csv ./csv/data.done
fi
python manage.py runserver -h 0.0.0.0
