"""Credentials for hw flask server."""
from os import getenv

import psycopg2
from dotenv import load_dotenv
from flask import Flask

from extras import DEFAULT_PORT

load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False

connection = psycopg2.connect(
    host=getenv('POSTGRES_HOST'),
    port=getenv('POSTGRES_PORT'),
    database=getenv('POSTGRES_DBNAME'),
    user=getenv('POSTGRES_USER'),
    password=getenv('POSTGRES_PASSWORD'),
)

FLASK_PORT = int(getenv('FLASK_PORT', default=DEFAULT_PORT))
