#!/bin/bash
python manage.py database migrate
python manage.py database upgrade
if [ ! -e ./csv/data.done ]
then
    echo "First launch, import..."
    python manage.py import_csv -c ./csv/data.csv
    cp ./csv/data.csv ./csv/data.done
    python manage.py backup_json -f ./csv/dbinit.json
fi

# TEMP! see above.
python manage.py backup_json -f ./csv/dbinit.json
python manage.py runserver -h 0.0.0.0
