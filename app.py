"""Crud hw flask server."""
import os

import dotenv
from flask import render_template, request
from psycopg2 import OperationalError
from psycopg2.sql import SQL, Literal
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session

import dbquery
import http_code
from models import Base, Meteodata


def get_db_url() -> str:
    dotenv.load_dotenv()
    PG_VARS = 'PG_HOST', 'PG_PORT', 'PG_USER', 'PG_PASSWORD', 'PG_DBNAME'
    credentials = {var: os.environ.get(var) for var in PG_VARS}
    return 'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'.format(**credentials)


from creds import FLASK_PORT, app, connection
from extras import WELCOME_PAGE, body_check

connection.autocommit = True

@app.route('/')
def welcomepage():
    data = meteo_get()
    stripped_data = dict(data[0][-1])
    # print(stripped_data)
    temperature = stripped_data['temperature']
    humidity = stripped_data['humidity']
    pressure = stripped_data['pressure']
    
    return render_template('index.html', title='home', temp=temperature, hum=humidity, pres=pressure)

@app.get('/meteodata/get')
def meteo_get():
    try:
        with connection.cursor() as cursor:
            cursor.execute(dbquery.QUERY_GET_DATA)
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
    """Post request handler used to delete conferences and links.

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
