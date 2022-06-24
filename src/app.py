from aiohttp import web
import sqlite3
import validators
import requests
import requests.exceptions
from http import HTTPStatus
import json
import string
import random

routes = web.RouteTableDef()

# get the ngrok tunnel url
def get_ngrok_url():
    """Function to get ngrok url"""
    url = "http://localhost:4040/api/tunnels"
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    return res_json["tunnels"][0]["public_url"]

def validate_url_format(longurl: str):
    """This function validates if the longurl is in a valid format"""
    return validators.url(longurl)

def validate_url(longurl: str):
    """This function validates if the longurl is a valid web address"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'}
        response = requests.get(longurl, headers=headers)
        return response.status_code == HTTPStatus.OK        
    except Exception as ex:
        print(ex)
        return False
        
def shorten_url(longurl: str):
    ngrok_url = get_ngrok_url()
    size = 6
    chars = string.ascii_uppercase + string.digits
    code = "".join(random.choice(chars) for _ in range(size))
    short_url = ngrok_url + "/" + code    
    try:
        cursor.execute(f"INSERT INTO URLSHORTNER VALUES (?, ?, ?)",(longurl, short_url, code,))        
    except Exception as ex:
        print(ex)
    return short_url

@routes.post("/shorten")
async def shorten(request):
    short_url = "Invalid URL"
    data = await request.post()
    longurl = data["url"]
    if validate_url_format(longurl) and validate_url(longurl):
        short_url = shorten_url(longurl)            
    return web.Response(text=short_url)
    

@routes.get("/{code}")
async def redirect_to_longurl(request):
    """Function to retrieve long URL based on code
    :param request: HTTP request
    """
    data = request.match_info["code"]    
    longurl = cursor.execute("SELECT longurl from URLSHORTNER where code = ?",(data,)).fetchone()        
    return web.HTTPFound(longurl[0])

if __name__ == "__main__":
    connection = sqlite3.connect("urlshortner.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS URLSHORTNER (longurl TEXT, shorturl TEXT, code TEXT UNIQUE)")
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="127.0.0.1", port=8000)
