import urllib.parse

import requests
import requests.exceptions
import json

from cloudbot import hook
from cloudbot.util.http import parse_soup


@hook.command("down", "offline", "up")
def down(text):
    """<url> - checks if <url> is online or offline

    :type text: str
    """

    if "://" not in text:
        text = 'http://' + text

    text = 'http://' + urllib.parse.urlparse(text).netloc

    try:
        r = requests.get(text)
        r.raise_for_status()
    except requests.exceptions.ConnectionError:
        return '{} seems to be down'.format(text)
    else:
        return '{} seems to be up'.format(text)


@hook.command()
def isup(text):
    """<url> - uses isup.me to check if <url> is online or offline

    :type text: str
    """
    headers = {'User-Agent': "PageCheck/1.0.0"}

    url = text.strip()

    # slightly overcomplicated, esoteric URL parsing
    _, auth, path, _, _ = urllib.parse.urlsplit(url)

    domain = auth or path

    try:
        response = requests.get('https://api.downfor.cloud/httpcheck/' + domain, headers=headers)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        return "Failed to get status."
    if response.status_code != requests.codes.ok:
        return "Failed to get status."

    results = json.loads(response.text)

    if results['isDown'] is None:
        return "Huh? That doesn't look like a site on the interweb."

    if results['isDown']:
        return "It's not just you. {} looks \x02\x034down\x02\x0f from here!".format(results['returnedUrl'])

    if not results['isDown']:
        return "It's just you. {} is \x02\x033up\x02\x0f.".format(results['returnedUrl'])
