from flask import jsonify, url_for
import re
import requests
import urllib
import demjson
import json

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def verify_json_single(body, *args):
    if body is None:
        return 'request body as an json object'
    for prop in args:
        if prop not in body:
            return prop
    return None

def verify_json(body, *args):
    for e in body:
        if e is None:
            return 'request body as an json object'
        for prop in args:
            if prop not in e:
                return prop
        return None

def generate_sitemap(app):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)

    links_html = "".join(["<li>" + y + "</li>" for y in links])
    return """
        <div style="text-align: center;">
        <img src='https://assets.breatheco.de/apis/img/4geeks/rigo-baby.jpg' />
        <h1>Hello Rigo!!</h1>
        This is your api home, remember to specify a real endpoint path like: <ul style="text-align: left;">"""+links_html+"</ul></div>"

def get_lat_long(html_source_code):
    regex = r"post_gpstobaidu\.php\?location=(-?\d+\.\d+)\,(\d+\.\d+)',"
    #regex = r"post_gpstobaidu\.php\?location=(-?\d+\.\d+)\,(\d+\.\d+)',"
    matches = re.finditer(regex, html_source_code, re.MULTILINE)
    latitude = None
    longitude = None
    for matchNum, match in enumerate(matches, start=1):
        latitude = match.group(2)
        longitude = match.group(1)

    if latitude is not None or longitude is not None:
        return { "latitude": latitude, "longitude": longitude }

    html_source_code = html_source_code[html_source_code.find("data: ")+7:]
    json_to_send = "{"+html_source_code[:html_source_code.find("}")+1]
    resp = requests.get("http://www.08gps.com/epost_minigps_wifi.php?"+urllib.parse.urlencode(demjson.decode(json_to_send)))
    # return None
    coord = json.loads(resp.text.encode().decode('utf-8-sig'))

    if coord is not None:
        return { "latitude": coord["lat"], "longitude": coord["lon"] }

    # If we are here it means the regex did not find
    # response = requests.get("http://www.08gps.com/epost_minigps_wifi.php?x=136-104-72bb-3ba9-c&ta=1&p=1&mt=1&needaddress=0&imei=359339075779555&ip=35.245.134.117&url=www.08gps.com&wifi=1:74:1082937503385560484;2:93:564395181913226170")
    # html_source_code = response.text

    return None