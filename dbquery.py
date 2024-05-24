"""Consts of queries for database."""
QUERY_GET_CONFS = """
select * from meteo.meteodata;

"""
QUERY_GET_PARTICS = 'select * from participants'

QUERY_CONFS_CREATE = """
insert into meteo.meteodata(temperature, humidity, pressure, created)
values ({temperature}, {humidity}, {pressure}, {created})
returning id
"""

QUERY_DELETE_CONF = 'delete from meteo.meteodata where id = {id} returning id'
