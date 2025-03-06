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

## Load database data
`python manage.py loaddata data.json`

## Run the development server
`python manage.py runserver`

The server should start running at `http://127.0.0.1:8000`
  
You can log in using the admin account.
username = admin
password=admin