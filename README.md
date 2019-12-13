# OpenSlides Write Service

Service worker for OpenSlides which accepts incomming requests to add, change or
delete data, checks and parses them and writes them to the event stream.

Requires Python 3.8.x (maybe also lower versions are working).

To setup run

    $ python -m venv .virtualenv
    $ source .virtualenv/bin/activate
    $ pip install --upgrade pip
    $ pip install --requirement requirements.txt

To start run

    $ python start.py

or

    $ pip install gunicorn==20.0.4
    $ gunicorn openslides_write_service.wsgi:application
