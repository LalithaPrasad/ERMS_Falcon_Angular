This is Employee record management app using falcon for api and angular 1.7 for
front-end. Flask is used to serve the fron-end. Since falcon is a minimal
framework, we need to use an external service to serve falcon api. Gunicorn can
be used for this purpose. Database is handled using sqlalchemy. Token based
authentication is used.

Backaend and front-end have to be started separately.
Backend can be started as follows:

    gunicorn ERMS_Falcon_API

In another terminal, front-end can be started as follows:

    flask run

Open browser and and access the url http://localhost:5000
