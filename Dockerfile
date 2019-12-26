FROM python:3.8-alpine

WORKDIR /srv/code

COPY requirements_production.txt .
RUN pip install --no-cache-dir --requirement requirements_production.txt

COPY openslides_write_service/ ./openslides_write_service/
COPY start.py .

EXPOSE 8000

ENV USE_CHEROOT_WSGI_SERVER 1

CMD [ "python", "start.py" ]
