from django import template

register = template.Library()


@register.simple_tag
def get_item(dictionary, **kwargs):
    from_city = kwargs['from_city']
    to_city = kwargs['to_city']
    date = kwargs['date']
    if (from_city + '-' + to_city, date) in dictionary:
        return '€' + str(dictionary.get((from_city + '-' + to_city, date)))
    return 'No flights'
