## A simple backend service that can generate and store 2D levels for Hotline Miami 2 <br>
As of `v0.1` it:
* can create a room graph and an image preview
* can authenticate users (super basic token auth, nothing fancy atm)
* provides an api for creating and viewing levels

## startup
example: <br>
`SERVER_PORT=8080 HOTLINE_ENV=local.env docker-compose up --build -d`

Required ENVs
* `HOTLINE_ENV` - name of the .env file which must contain the following variables
    * DB_USER
    * DB_PASS
    * DB_NAME
    * DB_HOST=db - *name of the postgres service in docker-compose.yml*
    * DJANGO_DEBUG= *True or False*
    * RABBITMQ_HOST=rabbit_mq - *name of the rabbitmq service in docker-compose.yml*
    * RABBITMQ_DEFAULT_USER
    * RABBITMQ_DEFAULT_PASS
    * RABBITMQ_DEFAULT_VHOST

Or use `template.env`
* `SERVER_PORT` - web server port to expose