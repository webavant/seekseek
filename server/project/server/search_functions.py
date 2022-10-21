import json
import xmltodict
import pafy
from youtube_search import YoutubeSearch

from genericpath import exists
from requests import request


def get_textfile(filepath, textstring=''):
    if exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    elif textstring:
        with open(filepath, 'w') as f:
            f.write(textstring)
            return textstring


def get_request(filepath, url, params={}):
    if exists(filepath):
        return get_textfile(filepath)
    else:
        return get_textfile(filepath, request('GET', url, params=params).text)


def do_search(platform, query):

    if platform == 'podcast':
        filename = f'search_podcast_{query}.json'
        url = 'https://itunes.apple.com/search'
        params = {'term': query, 'entity': 'podcast'}
        results = json.loads(get_request(filename, url, params)).get('results')

        selections = [({
            'platform': 'podcast',
            'url': l.get('feedUrl'),
            'name': l.get('collectionName')
        }) for l in results]

    elif platform == 'youtube':
        selections = [({
            'platform': 'youtube',
            'url': f'https://www.youtube.com/{l.get("url_suffix")}',
            'name': l.get("title")
        }) for l in YoutubeSearch(query).to_dict()]

    elif platform == 'radio':
        filename = f'search_radio_{query}.json'
        url = 'http://de1.api.radio-browser.info/json/stations/search'
        params = {'name': query}
        results = json.loads(get_request(filename, url, params))

        selections = [({'platform': 'radio', 'url': l.get(
            'url'), 'name': l.get('name')}) for l in results]

    return selections


def get_episodes(url):

    from hashlib import md5
    hex = md5(url.encode('utf-8')).hexdigest()
    x = xmltodict.parse(get_request(f'rss_{hex}.xml', url))
    selections = [({
        'platform': 'episode',
        'url': l.get('enclosure').get('@url'),
        'name': f'{l.get("pubDate")} – {l.get("title")}'
    }) for l in x.get('rss').get('channel').get('item')]
    return selections
