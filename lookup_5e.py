#!/usr/bin/env python
from bs4 import BeautifulSoup as bs
import requests
import sys


def stringify(text):
    return text.replace('<br>', '\n').replace('<br />', '\n')


def lookup5e(name):
    formatted_name = name.rstrip().title().replace(' ', '_')
    url = 'https://roll20.net/compendium/dnd5e/{:s}'.format(formatted_name)
    page = requests.get(url)
    if page.status_code != 200:
        print('{:s} not found.'.format(name))
        print(page)
        return
    soup = bs(page.text, 'html.parser')
    for attr in soup.findAll(attrs={'class': 'col-md-3 attrName'}):
        text = (stringify(attr.text) + ': ' +
                stringify(attr.find_next(attrs={'class':
                                                'value'}).text))
        print(text)
    print('\n\nDescription\n===========================\n')
    for val in soup.findAll(attrs={'id': 'origpagecontent',
                                   'type': 'text/html'}):
        print(stringify(val.text))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        lookup5e(text)
    
