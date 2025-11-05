@echo off
echo Collecting static files...
python manage.py collectstatic --noinput
echo.
echo Static files collected successfully!
echo Now upload the staticfiles folder to PythonAnywhere
pause
