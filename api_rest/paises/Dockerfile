FROM icorrea/flask-restplus:0.13.0-alpine3.10

RUN mkdir -p /app/api_paises

WORKDIR /app

COPY api_paises /app/api_paises

COPY wsgi.* /app/

EXPOSE 5000

CMD ["uwsgi", "--ini", "/app/wsgi.ini"]
