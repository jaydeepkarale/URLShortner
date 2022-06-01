"""Main file for performing url shortening"""
import json
import random
import string
from http import HTTPStatus
from urllib.request import urlopen

import requests
import validators
from aiohttp import web

# use a dictionary for now instead of a DB
url_mapping = {}

routes = web.RouteTableDef()

# get the ngrok tunnel url
def get_ngrok_url():
    """Function to get ngrok url"""
    url = "http://localhost:4040/api/tunnels"
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    return res_json["tunnels"][0]["public_url"]


# perform validation to check if URL is in correct format
def validate_long_url_format(url: str):
    """Function to validate if url is in correct format
    :param url: The long url to be shortened
    """
    response = validators.url(url)
    return response
    print(response)


# shorten the url by generating a 6 character code & appending to base url
def shorten_url(url: str):
    """Function to shorten url
    :param url: The long url to be shortened
    """
    ngrok_url = get_ngrok_url()
    size = 6
    chars = string.ascii_uppercase + string.digits
    code = "".join(random.choice(chars) for _ in range(size))
    short_url = ngrok_url + "/" + code
    url_mapping[code] = url
    return short_url


@routes.post("/shorten")
async def write_mapping_to_db(request):
    """Function to write longurl-shorturl mapping to dictionary
    :param request: HTTP request
    """
    data = await request.post()
    longurl = data["url"]
    if validate_long_url_format(longurl) and validate_url(longurl):
        short_url = shorten_url(longurl)
    return web.Response(text=short_url)


@routes.get("/{code}")
async def do_the_magic(request):
    """Function to retrieve long URL based on code
    :param request: HTTP request
    """
    data = request.match_info["code"]
    longurl = url_mapping[data]
    print(longurl)
    return web.HTTPFound(longurl)


# perform validation to check URL is a valid website
def validate_url(url: str):
    """Function to validate if long url is a valid website
    :param url: long url to be shortened
    """
    try:
        print(requests.get(url))
        response = urlopen(url).getcode()
        if response == HTTPStatus.OK:
            print(response)
            return True
    except Exception as ex:
        print(ex)
    return False


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=8000)
