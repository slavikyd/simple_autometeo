"""Sirius meteo_api REST handler."""
import os

import dotenv
from flask import render_template, request
from psycopg2 import OperationalError
from psycopg2.sql import SQL, Literal

import dbquery
import http_code
from creds import FLASK_PORT, app, connection


def get_db_url() -> str:
    """Databse connecntion handler function.

    Returns:
        str: link for db connection.
    """
    dotenv.load_dotenv()
    pg_vars = (
        'POSTGRES_HOST',
        'POSTGRES_PORT',
        'POSTGRES_USER',
        'POSTGRES_PASSWORD',
        'POSTGRES_DBNAME',
    )
    credentials = {variab: os.environ.get(variab) for variab in pg_vars}
    return (
        'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}?options=--search_path=meteo'.format(**credentials)
    )


connection.autocommit = True


@app.route('/')
def welcomepage() -> None:
    """Welcoming webpage generator.

    Returns:
        rendered template of main page.
    """
    return render_template('index.html', title='home')


@app.get('/meteodata/get')
def meteo_get_single():
    """Last db record getter.

    Returns:
        dict of values and http_code if success or http_code 500 if failed
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(dbquery.QUERY_GET_DATA_SINGLE)
            return cursor.fetchall(), http_code.OK
    except OperationalError:
        return http_code.SERVER_ERROR


@app.get('/meteodata/get_all')
def meteo_get():
    """Db record getter.

    Returns:
        dict of values and http_code if success or http_code 500 if failed
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(dbquery.QUERY_GET_DATA)
            return cursor.fetchall(), http_code.OK
    except OperationalError:
        return http_code.SERVER_ERROR


@app.post('/meteodata/create')
def create_meteodata():
    """Post request handler for data.

    Returns:
        str: empty string
        int: http-code answer
    """
    body = request.json

    temperature = body['temperature']
    humidity = body['humidity']
    pressure = body['pressure']
    created = body['created']

    query = SQL(dbquery.QUERY_DATA_CREATE).format(
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
    """Post request handler used to delete data.

    Returns:
        str: empty str
        int: http-code answer
    """
    body = request.json

    id_ = body['id']

    delete_conference = SQL(dbquery.QUERY_DELETE_DATA).format(id=Literal(id_))

    with connection.cursor() as cursor:
        cursor.execute(delete_conference)
        result = cursor.fetchall()

    if len(result) == 0:
        return '', http_code.NOT_FOUND

    return '', http_code.NO_CONTENT


if __name__ == '__main__':
    app.run(port=FLASK_PORT)
