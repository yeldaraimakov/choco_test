import logging
import requests
from datetime import datetime, timedelta
from django.core.cache import cache
from celery.decorators import task

DAYS = 30
DIRECTIONS = (('ALA', 'TSE'), ('TSE', 'ALA'), ('ALA', 'MOW'), ('MOW', 'ALA'), ('ALA', 'CIT'),
              ('CIT', 'ALA'), ('TSE', 'MOW'), ('MOW', 'TSE'), ('TSE', 'LED'), ('LED', 'TSE'))

logger = logging.getLogger('info_logger')


@task(name="update_prices")
def update_prices():
    """
    Updates ticket prices for 10 directions every midnight
    Saves prices in cache
    """
    logger.info("Update price task started")

    cache.clear()
    logger.info('Cache was cleared')

    from_date = datetime.today().strftime('%d/%m/%Y')
    to_date = (datetime.today() + timedelta(days=DAYS)).strftime('%d/%m/%Y')

    for direction in DIRECTIONS:
        update_direction_price(direction[0], direction[1], from_date, to_date)

    logger.info("All prices were updated")


def update_direction_price(from_city, to_city, from_date, to_date):
    """
    Updates ticket prices for one direction
    """
    req = requests.get('https://api.skypicker.com/flights',
                       params={'fly_from': from_city, 'fly_to': to_city, 'date_from': from_date,
                               'date_to': to_date, 'partner': 'picky'})
    cheap_tickets = dict()

    if req.status_code == 200:
        tickets = req.json()['data']

        for ticket in tickets:
            date = datetime.fromtimestamp(ticket['dTime']).strftime("%d/%m/%Y")
            price = ticket['price']

            if date not in cheap_tickets:
                cheap_tickets[date] = price
            else:
                cheap_tickets[date] = min(cheap_tickets[date], price)

    cache.set(from_city + '-' + to_city, cheap_tickets, timeout=None)
    logger.info("Ticket prices from %s to %s were updated" % (from_city, to_city))
