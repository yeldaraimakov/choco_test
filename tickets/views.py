from django.shortcuts import render
from datetime import datetime, timedelta
from django.core.cache import cache
from tickets.tasks import DIRECTIONS, DAYS


def home(request):
    prices = dict()
    for direction in DIRECTIONS:
        direct = direction[0] + '-' + direction[1]
        prices[direct] = []
        cheap_tickets = cache.get(direct, {})
        for date, price in cheap_tickets.items():
            prices[(direct, date)] = price

    date = datetime.today()
    to_date = date + timedelta(days=DAYS)
    dates = []
    while date <= to_date:
        dates.append(date.strftime('%d/%m/%Y'))
        date += timedelta(days=1)

    return render(request, 'home.html', context={'prices': prices, 'directions': DIRECTIONS, 'dates': dates})
