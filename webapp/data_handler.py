"""Module with average calculating functions."""
from datetime import datetime


def avgs_by_date(test_data):
    """Average data counter per day.

    Args:
        test_data (_type_): list of dicts with data

    Returns:
        _type_: dict with sorted per day values
    """
    daily_values = {}
    daily_counts = {}

    for data in test_data:
        date = datetime.strptime(data['created'], '%a, %d %b %Y %H:%M:%S %Z').date()

        if date not in daily_values:
            daily_values[date] = {'temperature': 0, 'pressure': 0, 'humidity': 0}
            daily_counts[date] = {'temperature': 0, 'pressure': 0, 'humidity': 0}

        daily_values[date]['temperature'] += data['temperature']
        daily_values[date]['pressure'] += data['pressure']
        daily_values[date]['humidity'] += data['humidity']

        daily_counts[date]['temperature'] += 1
        daily_counts[date]['pressure'] += 1
        daily_counts[date]['humidity'] += 1

    daily_averages = {}
    for date in daily_values:
        daily_averages[date] = {
            'average_temperature': round(daily_values[date]['temperature'] / daily_counts[date]['temperature'], 2),
            'average_pressure': round(daily_values[date]['pressure'] / daily_counts[date]['pressure'], 2),
            'average_humidity': round(daily_values[date]['humidity'] / daily_counts[date]['humidity'], 2),
        }

    return daily_averages


def avgs_by_month(test_data):
    """Average data counter per month.

    Args:
        test_data (_type_): list of dicts with data

    Returns:
        _type_: dict with sorted per month values
    """
    monthly_values = {}
    monthly_counts = {}

    for data in test_data:
        date = datetime.strptime(data['created'], '%a, %d %b %Y %H:%M:%S %Z')
        month_year = (date.year, date.month)

        if month_year not in monthly_values:
            if month_year[0] != datetime.today().year:
                continue
            monthly_values[month_year] = {'temperature': 0, 'pressure': 0, 'humidity': 0}
            monthly_counts[month_year] = {'temperature': 0, 'pressure': 0, 'humidity': 0}

        monthly_values[month_year]['temperature'] += data['temperature']
        monthly_values[month_year]['pressure'] += data['pressure']
        monthly_values[month_year]['humidity'] += data['humidity']

        monthly_counts[month_year]['temperature'] += 1
        monthly_counts[month_year]['pressure'] += 1
        monthly_counts[month_year]['humidity'] += 1

    monthly_averages = {}
    for month_year in monthly_values:
        monthly_averages[month_year] = {
            'average_temperature': monthly_values[month_year]['temperature'] / monthly_counts[month_year]['temperature'],
            'average_pressure': monthly_values[month_year]['pressure'] / monthly_counts[month_year]['pressure'],
            'average_humidity': monthly_values[month_year]['humidity'] / monthly_counts[month_year]['humidity'],
        }

    return monthly_averages


def values_by_hours(test_data):
    """Average data counter per hour.

    Args:
        test_data (_type_): list of dicts with data

    Returns:
        _type_: dict with sorted per hour values
    """
    hourly_values = {}
    hourly_counts = {}

    for data in test_data:
        today = datetime.strptime(data['created'], '%a, %d %b %Y %H:%M:%S %Z').date()
        if today.day != datetime.today().day:
            continue
        date = datetime.strptime(data['created'], '%a, %d %b %Y %H:%M:%S %Z')
        day_hour = (date.day, date.hour)

        if day_hour not in hourly_counts:
            hourly_values[day_hour] = {'temperature': 0, 'pressure': 0, 'humidity': 0}
            hourly_counts[day_hour] = {'temperature': 0, 'pressure': 0, 'humidity': 0}

        hourly_values[day_hour]['temperature'] += data['temperature']
        hourly_values[day_hour]['pressure'] += data['pressure']
        hourly_values[day_hour]['humidity'] += data['humidity']

        hourly_counts[day_hour]['temperature'] += 1
        hourly_counts[day_hour]['pressure'] += 1
        hourly_counts[day_hour]['humidity'] += 1

        hourly_averages = {}
        for day_hour in hourly_values:
            hourly_averages[day_hour] = {
                'average_temperature': hourly_values[day_hour]['temperature'] / hourly_counts[day_hour]['temperature'],
                'average_pressure': hourly_values[day_hour]['pressure'] / hourly_counts[day_hour]['pressure'],
                'average_humidity': hourly_values[day_hour]['humidity'] / hourly_counts[day_hour]['humidity'],
            }

    return hourly_averages
