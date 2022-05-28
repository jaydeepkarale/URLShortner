import http
import validators
from urllib.request import urlopen
from http import HTTPStatus
import string
import random
from aiohttp import web
from pyngrok import ngrok
import requests
import json

# this is domain we need to buy
base_url = "http://127.0.0.1:8080/"
url_mapping  = {}

routes = web.RouteTableDef()

def get_ngrok_url():
    url = "http://localhost:4040/api/tunnels"
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    return res_json["tunnels"][0]["public_url"]


# perform validation to check if URL is in correct format
def validate_long_url_format(url: str):
    response = validators.url(url)
    return response
    print(response)

# shorten the url by generating a 6 character code & appending to base url
def shorten_url(url: str):       
    ngrok_url = get_ngrok_url()
    size = 6
    chars=string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(size))
    short_url  = ngrok_url + "/" +code
    url_mapping[code] = url
    return short_url

@routes.post('/shorten')
async def write_mapping_to_db(request):
    
    data  = await request.post()
    longurl = data['url']
    if validate_long_url_format(longurl) and validate_url(longurl):
        short_url = shorten_url(longurl)
    return web.Response(text=short_url)

@routes.post('/{code}')
async def do_the_magic(request):
    data  = request.match_info["code"]
    longurl = url_mapping[data]
    print(longurl)
    return web.HTTPFound(longurl)
    

# perform validation to check URL is a valid website
def validate_url(url: str):
    try:
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