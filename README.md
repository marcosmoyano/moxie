## 0. About

Moxie Take home exercise

## 1. Goals

The goal of this take-home assignment is to help us assess your ability to:

1. Design sensible, robust database table schemas
2. Write RESTful CRUD functionality for the given tables

## 2. Constrains

Moxie uses PostgreSQL but here I'm using SQLite for speed of development. This lets me move faster without the need to create a Dockerfile
and docker-compose.yml to have the services talking to each other.

## 3. Assumptions / Things left out due to time constrain

1. There are no users nor authentication required to use these apis.
2. A MedSpa can have as many appointments as they want. Meaning, we don't check for availability against time nor services.
3. When creating an appointment, we assume the services passed in belong to the medspa that's also passed in. No validation is done here.
4. SQLite does not support an ArrayField so I've turned the service type into a M2M field. If I were to use PG I'd use an ArrayField here.

## 4. Prerequisites

[Poetry](https://python-poetry.org/) is required to setup the project.

## 5. Project setup

After cloning the repo (`git clone git@github.com:marcosmoyano/moxie.git`), cd into it and run:

```sh
poetry install
```

Move into the moxie follder and run the migrations:

```sh
cd moxie/
python manage.py migrate
```

Collect static files and create a superuser to be able to use the Django admin or the DRF Browsable API:

```sh
python manage collectstatic
python manage createsuperuser
```

## 6. Running tests

Inside the moxie, run pytest

```sh
pytest
```

## 7. Using the API

Run the development service

```sh
python manage.py runserver
```

The API is intended to be used against a subset of models and model fields, meaning not everything is exposed to the API. At least a MedSpa is required. Login to the Django admin with your superuser and create a MedSpa. If you were successful the MedSpa would have an id of 1. Will use that for the rest of the example

Creating a service for your MedSpa. I'll be using the `requests` python module but feel free to use any other client that better suites you.

```python

In [1]: import requests

In [2]: data = {"medspa_id": 1, "name": "Peel", "price": "500.00", "duration": "00:30:00", "description"
   ...: : "Peel Description"}

In [3]: response = requests.post("http://localhost:8000/service/", json=data, headers={"Content-Type": "
   ...: application/json"})

In [4]: response.status_code
Out[4]: 201

In [5]: response.json()
Out[5]:
{'id': 1,
 'medspa': {'id': 1,
  'name': 'Cirtrus Aesthetic',
  'address': 'road',
  'phone_number': '+15174996412',
  'email_address': 'jessica@citrysaestheticis.com'},
 'name': 'Peel',
 'description': 'Peel Description',
 'price': '500.00',
 'duration': '00:30:00'}
```

You can get the service by its id. 1 is the service `id`.

```python
In [7]: response = requests.get("http://localhost:8000/services/1/")

In [8]: response.status_code
Out[8]: 200

In [9]: response.json()
Out[9]:
{'id': 1,
 'medspa': {'id': 1,
  'name': 'Cirtrus Aesthetic',
  'address': 'road',
  'phone_number': '+15174996412',
  'email_address': 'jessica@citrysaestheticis.com'},
 'name': 'Peel',
 'description': 'Peel Description',
 'price': '500.00',
 'duration': '00:30:00'}
```

You can also list the services for a given MedSpa. 1 is the MedSpa `id`.

```python

In [10]: response = requests.get("http://localhost:8000/1/services/")

In [11]: response.json()
Out[11]:
[{'id': 1,
  'medspa': {'id': 1,
   'name': 'Cirtrus Aesthetic',
   'address': 'road',
   'phone_number': '+15174996412',
   'email_address': 'jessica@citrysaestheticis.com'},
  'name': 'Peel',
  'description': 'Peel Description',
  'price': '500.00',
  'duration': '00:30:00'}]
```

You can change the service (name, description, price and duration).

```python

In [13]: response = requests.patch("http://localhost:8000/services/1/", json=data, headers={"Content-Typ
    ...: e": "application/json"})

In [14]: response.json()
Out[14]:
{'id': 1,
 'medspa': {'id': 1,
  'name': 'Cirtrus Aesthetic',
  'address': 'road',
  'phone_number': '+15174996412',
  'email_address': 'jessica@citrysaestheticis.com'},
 'name': 'Peeel',
 'description': 'New Description',
 'price': '540.00',
 'duration': '00:45:00'}
```

Now lets create an appointment for this MedSpa using this service.

```python

In [17]: data = {"medspa_id": 1, "start_time": "2024-10-22 19:00:00", "services": [1]}

In [18]: response = requests.post("http://localhost:8000/appointment/", json=data, headers={"Content-Typ
    ...: e": "application/json"})

In [19]: response.json()
Out[19]:
{'id': 1,
 'medspa': {'id': 1,
  'name': 'Cirtrus Aesthetic',
  'address': 'road',
  'phone_number': '+15174996412',
  'email_address': 'jessica@citrysaestheticis.com'},
 'start_time': '2024-10-22T19:00:00Z',
 'services': [{'id': 1,
   'medspa': {'id': 1,
    'name': 'Cirtrus Aesthetic',
    'address': 'road',
    'phone_number': '+15174996412',
    'email_address': 'jessica@citrysaestheticis.com'},
   'name': 'Peeel',
   'description': 'New Description',
   'price': '540.00',
   'duration': '00:45:00'}],
 'status': 'Scheduled',
 'total_duration': '00:45:00',
 'total_price': '540.00'}
```

You can grab the appointment by its `id`. 1 is the appointment `id`.

```python

In [23]: response = requests.get("http://localhost:8000/appointments/1/")

In [24]: response.json()
Out[24]:
{'id': 1,
 'medspa': {'id': 1,
  'name': 'Cirtrus Aesthetic',
  'address': 'road',
  'phone_number': '+15174996412',
  'email_address': 'jessica@citrysaestheticis.com'},
 'start_time': '2024-10-22T19:00:00Z',
 'services': [{'id': 1,
   'medspa': {'id': 1,
    'name': 'Cirtrus Aesthetic',
    'address': 'road',
    'phone_number': '+15174996412',
    'email_address': 'jessica@citrysaestheticis.com'},
   'name': 'Peeel',
   'description': 'New Description',
   'price': '540.00',
   'duration': '00:45:00'}],
 'status': 'Scheduled',
 'total_duration': '00:45:00',
 'total_price': '540.00'}
```

Lets mark the appointment as `Completed`.

```python

In [26]: response = requests.patch("http://localhost:8000/appointment/1/change-status/", json={"status":
    ...:  "Completed"}, headers={"Content-Type": "application/json"})

In [27]: response.json()
Out[27]:
{'status': 'Completed',
 'medspa': {'id': 1,
  'name': 'Cirtrus Aesthetic',
  'address': 'road',
  'phone_number': '+15174996412',
  'email_address': 'jessica@citrysaestheticis.com'},
 'services': [{'id': 1,
   'medspa': {'id': 1,
    'name': 'Cirtrus Aesthetic',
    'address': 'road',
    'phone_number': '+15174996412',
    'email_address': 'jessica@citrysaestheticis.com'},
   'name': 'Peeel',
   'description': 'New Description',
   'price': '540.00',
   'duration': '00:45:00'}],
 'start_time': '2024-10-22T19:00:00Z',
 'total_price': 540.0,
 'total_duration': '2700.0'}
```

You can also list the appointments and filter them by either status or start_date (or both combined).
These 4 examples return the same result.

```python
In [28]: response = requests.get("http://localhost:8000/appointments/")
In [29]: response = requests.get("http://localhost:8000/appointments/", params={"status": "Completed"})
In [30]: response = requests.get("http://localhost:8000/appointments/", params={"start_date": "2024-20-22"})
In [31]: response = requests.get("http://localhost:8000/appointments/", params={"status": "Completed", "start_date": "2024-20-22"})

Out[31]:
[{'id': 1,
  'medspa': {'id': 1,
   'name': 'Cirtrus Aesthetic',
   'address': 'road',
   'phone_number': '+15174996412',
   'email_address': 'jessica@citrysaestheticis.com'},
  'start_time': '2024-10-22T19:00:00Z',
  'services': [{'id': 1,
    'medspa': {'id': 1,
     'name': 'Cirtrus Aesthetic',
     'address': 'road',
     'phone_number': '+15174996412',
     'email_address': 'jessica@citrysaestheticis.com'},
    'name': 'Peeel',
    'description': 'New Description',
    'price': '540.00',
    'duration': '00:45:00'}],
  'status': 'Completed',
  'total_duration': '00:45:00',
  'total_price': '540.00'}]

```
