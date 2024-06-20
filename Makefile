.PHONY: migrations, migrate, su, test, run, shell, app

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

su:
	python manage.py createsuperuser

test:
	python manage.py test

run:
	python manage.py runserver 0.0.0.0:80

shell:
	python manage.py shell

app:
	python manage.py startapp ${name}