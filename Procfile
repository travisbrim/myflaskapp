web: gunicorn myflaskapp.app:create_app\(\) -b 0.0.0.0:$PORT -w $WEB_CONCURRENCY
release: flask db upgrade
