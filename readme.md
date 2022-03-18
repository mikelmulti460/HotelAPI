# Booking HotelAPI
## 

[![N|Solid](https://svgshare.com/i/eCY.svg)](#)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](#)

API to make hotel reservations

- Made with Django Rest Framework
- Scalable

## Features

- Creation of rooms
- creation of reservations
- check dates
- Automatic calculation of fees

## Endpoints

- **api/v1/rooms/** - Access to room-list
    -- The api/v1/ endpoint was chosen to have a better control of the api updates
    -- The /api/v1/rooms/ endpoint was chosen to start a reservation process that is consistent     with the relationships in the models
       rooms
- **api/v1/rooms/<int:id>/** - Access to especific room
- **api/v1/rooms/<int:id>/booking/** - Access to booking list
    -- This endpoint was chosen to continue the booking process so that the front-end developer has data on current bookings.
- **api/v1/rooms/<int:id>/booking/<int:id>** - This endpoint was chosen to facilitate access to the reservation and avoid additional parameters in the query


## Installation

HotelsApi requires [Python](https://www.python.org/downloads/) v3.8+ to run.

Install the dependencies and devDependencies and start the server.

```sh
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver localhost:8000
```

## License

MIT

**Free Software, Hell Yeah!**
