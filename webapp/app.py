"""Main webpage code."""
import os

import dotenv
import plotly.graph_objects as go
import requests
from flask import Flask, render_template, request
from psycopg2 import OperationalError
from psycopg2.sql import SQL, Literal

import data_handler
import dbquery
import http_code
from creds import FLASK_PORT, app, connection

URL = 'http://5.101.180.71:5000'
URL_GET = 'http://5.101.180.71:5000/meteodata/get'
URL_GET_ALL = 'http://5.101.180.71:5000/meteodata/get_all'
DELAY_REQ = 120

NOT_FOUND_PAGE = '<h1>server is down, sorry</h1>'


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
    credentials = {var: os.environ.get(var) for var in pg_vars}
    return 'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}?options=--search_path=meteo'.format(
        **credentials,
    )


connection.autocommit = True
server = Flask(__name__)


@app.route('/')
def welcomepage():
    """Welcoming webpage generator.

    Returns:
        rendered template of main page.
    """
    try:
        data = requests.get(URL_GET, timeout=DELAY_REQ)
    except Exception:
        return NOT_FOUND_PAGE, http_code.SERVER_ERROR

    data = data.json()
    temperature = data[0]['temperature']
    humidity = data[0]['humidity']
    pressure = data[0]['pressure']
    created = data[0]['created']

    return render_template(
        'index.html',
        title='home',
        temp=temperature,
        hum=humidity,
        pres=pressure,
        created=created,
    )


@app.get('/meteodata/get')
def meteo_get_single():
    """Last db record getter.

    Returns:
        dict of values and http_code if success or http_code 500 if failed
    """
    try:
        data = requests.get(URL_GET, timeout=DELAY_REQ)
    except Exception:
        return http_code.SERVER_ERROR
    return data.json(), http_code.OK


@app.get('/meteodata/get_all')
def meteo_get():
    """Db all record getter.

    Returns:
        dict of values and http_code if success or http_code 500 if failed
    """
    try:
        data = requests.get(URL_GET_ALL, timeout=DELAY_REQ)
    except Exception:
        return http_code.SERVER_ERROR
    return data.json(), http_code.OK


@app.get('/inner/meteodata/get_all')
def meteo_get_inner():
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


@app.get('/inner/meteodata/get')
def meteo_get_single_inner():
    """Db record getter.

    Returns:
        dict of values and http_code if success or http_code 500 if failed
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(dbquery.QUERY_GET_DATA_SINGLE)
            return cursor.fetchall(), http_code.OK
    except OperationalError:
        return http_code.SERVER_ERROR



@app.post('/inner/meteodata/create')
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


@app.delete('/inner/meteodata/delete')
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


@app.route('/meteodata/graph', methods=['GET', 'POST'])
def plot():
    """Plot generator.

    Returns:
        _type_: webpage with interactive plots
    """
    graph = request.form.get('graph')
    try:
        data = requests.get(URL_GET_ALL, timeout=DELAY_REQ)
    except Exception:
        return http_code.SERVER_ERROR
    data = data.json()
    temp = data_handler.avgs_by_date(data)

    x = [key.day for key in temp.keys()]

    if graph == 'Temperature by days':
        temp = data_handler.avgs_by_date(data)
        dict_values = list(temp.values())
        x = [key.day for key in temp.keys()]
        y = [int(temp['average_temperature']) for temp in dict_values]
        fig = go.Figure(data=go.Scatter(x=x, y=y))
        fig.update_layout(title='temperature_by_days')
    elif graph == 'Temperature by months':
        temp = data_handler.avgs_by_month(data)
        dict_values = list(temp.values())
        x = [key[1] for key in temp.keys()]
        y = [int(temp['average_temperature']) for temp in dict_values]
        fig = go.Figure(data=go.Scatter(x=x, y=y))
        fig.update_layout(title='temperature_by_months')
    elif graph == 'Temperature by hours':
        temp = data_handler.values_by_hours(data)
        dict_values = list(temp.values())
        x = [key[1] for key in temp.keys()]
        y = [int(temp['average_temperature']) for temp in dict_values]
        fig = go.Figure(data=go.Scatter(x=x, y=y))
        fig.update_layout(title='temperature_by_hours')
    elif graph == 'Pressure by days':
        temp = data_handler.avgs_by_date(data)
        dict_values = list(temp.values())
        x = [key.day for key in temp.keys()]
        y = [int(temp['average_pressure']) for temp in dict_values]
        fig = go.Figure(data=go.Scatter(x=x, y=y))
        fig.update_layout(title='pressure_by_days')
    elif graph == 'Pressure by months':
        temp = data_handler.avgs_by_date(data)
        dict_values = list(temp.values())
        x = [key[1] for key in temp.keys()]
        y = [int(temp['average_pressure']) for temp in dict_values]
        fig = go.Figure(data=go.Scatter(x=x, y=y))
        fig.update_layout(title='pressure_by_months')
    elif graph == 'Humidity by days':
        temp = data_handler.avgs_by_date(data)
        dict_values = list(temp.values())
        x = [key.day for key in temp.keys()]
        y = [int(temp['average_humidity']) for temp in dict_values]
        fig = go.Figure(data=go.Scatter(x=x, y=y))
        fig.update_layout(title='humidity_by_days')
    elif graph == 'Humidity by months':
        temp = data_handler.avgs_by_date(data)
        dict_values = list(temp.values())
        x = [key[1] for key in temp.keys()]
        y = [int(temp['average_humidity']) for temp in dict_values]
        fig = go.Figure(data=go.Scatter(x=x, y=y))
        fig.update_layout(title='humidity_by_months')
    else:
        temp = data_handler.values_by_hours(data)
        dict_values = list(temp.values())
        x = [key[1] for key in temp.keys()]
        y = [int(temp['average_temperature']) for temp in dict_values]
        fig = go.Figure(data=go.Scatter(x=x, y=y))
        fig.update_layout(title='temperature_by_hours')

    plot_div = fig.to_html(full_html=False)

    return render_template('graph.html', plot_div=plot_div)


if __name__ == '__main__':
    app.run(port=FLASK_PORT)
