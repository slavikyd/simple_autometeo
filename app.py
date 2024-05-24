"""Crud hw flask server."""
from flask import request
from psycopg2 import OperationalError
from psycopg2.sql import SQL, Literal

import dbquery
import http_code
from creds import FLASK_PORT, app, connection
from extras import WELCOME_PAGE, body_check

connection.autocommit = True


@app.get('/')
def welcomingpage():
    """Welcome page handler.

    Returns:
        str: html string of welcome page
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(dbquery.QUERY_GET_CONFS)
            return cursor.fetchall(), http_code.OK
    except OperationalError:
        return http_code.SERVER_ERROR


@app.post('/meteodata/create')
def create_meteodata():
    """Post request handler for conferences.

    Returns:
        str: empty string
        int: http-code answer
    """
    body = request.json

    temperature = body['temperature']
    humidity = body['humidity']
    pressure = body['pressure']
    created = body['created']


    query = SQL(dbquery.QUERY_CONFS_CREATE).format(
        temperature=Literal(temperature),
        humidity=Literal(humidity),
        pressure=Literal(pressure),
        created=Literal(created),
        )

    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()

    return result, http_code.OK




@app.delete('/meteodata/delete')
def delete_meteodata():
    """Post request handler used to delete conferences and links.

    Returns:
        str: empty str
        int: http-code answer
    """
    body = request.json

    id_ = body['id']

    delete_conference = SQL(dbquery.QUERY_DELETE_CONF).format(id=Literal(id_))

    with connection.cursor() as cursor:
        cursor.execute(delete_conference)
        result = cursor.fetchall()

    if len(result) == 0:
        return '', http_code.NOT_FOUND

    return '', http_code.NO_CONTENT


if __name__ == '__main__':
    app.run(port=FLASK_PORT)
