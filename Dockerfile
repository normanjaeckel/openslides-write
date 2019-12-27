FROM python:3.8-alpine

WORKDIR /srv/code

COPY requirements_production.txt .
RUN pip install --no-cache-dir --requirement requirements_production.txt

EXPOSE 8000

# See https://pythonspeed.com/articles/gunicorn-in-docker/
CMD [ "gunicorn", "--bind=0.0.0.0:8000", "--worker-tmp-dir=/dev/shm", "openslides_write_service.wsgi:application" ]

COPY openslides_write_service/ ./openslides_write_service/
