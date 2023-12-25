# delivery-svc
A project to calculate shipping cost for a parcel

## Start a new project:

Image for the django_app container is build from Dockerfile.  
Celery-worker, celery-beat and flower containers use the same image as django_app.

Containers up:
```
docker-compose up django-db -d && sleep 10 && docker-compose up -d
```
Note: Wait is related to the launch of the database,  
the codependent containers are waiting for readiness.

Grant access rights for test database:
```
docker exec -it django_db mysql -u root -ppassword -e \
"GRANT ALL PRIVILEGES ON test_delivery.* TO 'mysql_user';" delivery
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

Running unit tests:
```
python manage.py test
```

## A project is self-documented, to view all the endpoints and their descriptions, go to the url:

```
http://localhost:8080/swagger/
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
