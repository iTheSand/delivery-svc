# delivery-svc
A project to calculate the shipping cost for a parcel

## Start a new project:

Image for the django_app container is build from Dockerfile.  
Celery-worker, celery-beat and flower containers use the same image as django_app.

Containers up:

```
docker-compose up django-db -d && sleep 10 && docker-compose up -d
```

Get in to the django_app container Shell:

```
docker-compose run --rm django_app /bin/bash
```

Make migrations:

```
python manage.py makemigrations
python manage.py migrate
```


## The project uses utilities to verify compliance with standards  and code quality requirements:

Instructions for local startup:
```
docker-compose run --rm django_app /bin/bash
```

Running a check using isort, black, flake8 and pylint:
```
python -m nox
```

Running auto-formatting using isort and black:
```
python -m nox -k format_task
```
