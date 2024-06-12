"""Consts of queries for database."""
QUERY_GET_DATA = """
select * from meteo.meteodata;

"""
QUERY_GET_DATA_SINGLE = """
select * from meteo.meteodata limit 1;

"""
QUERY_DATA_CREATE = """
insert into meteo.meteodata(temperature, humidity, pressure, created)
values ({temperature}, {humidity}, {pressure}, {created})
returning id
"""

QUERY_DELETE_DATA = 'delete from meteo.meteodata where id = {id} returning id'
