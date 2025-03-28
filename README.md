# django_storefront

## Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

## Install project dependencies

  `pip install -r requirements.txt`

## Set up the database
`python manage.py migrate`

## Create an admin account
`python manage.py createsuperuser`

## Run the development server
`daphne -b 127.0.0.1 -p 8000 django_storefront.asgi:application`

The server should start running at `http://127.0.0.1:8000`