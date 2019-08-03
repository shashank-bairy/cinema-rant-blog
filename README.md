# CinemaRant

A website for booking cinema tickets which seeks to improve the cinema occupancy rates across the country.

## Installation

Fork the repository to your github profile and clone the repository to your local system.

Once you have coloned the repository. Perform

```bash
pip install -r requirements.txt
```

This installs all the necessary package dependencies if not already installed.

Next run the migrations

```bash
python manage.py migrate
```

**Make sure that you have connected the required database**

- sqlite3 in Development mode
- Postgres in Production mode
  ( [**Instructions to setup Postgres**](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04) )

Create admin user using below command and following the instructions after that

```bash
python manage.py createsuperuser
```

## Usage

To run the app

```bash
python manage.py runserver
```
