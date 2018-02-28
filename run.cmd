pushd %~dp0"
start "" cmd /k "venv\Scripts\activate&&python manage.py runserver"
