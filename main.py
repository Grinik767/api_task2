import sys

import os
from func import zoom_toponym_two_object, get_max_zoom, count_distance

import requests
from PIL import Image, ImageDraw, ImageFont

toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    pass
else:
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"].split()
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    address_ll = ','.join(toponym_coodrinates)

    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        pass
    else:
        json_org = response.json()
        '''with open('test.json', 'w', encoding='utf-8') as f:
            f.write(str(json_org))'''
        organization = json_org['features'][0]
        comp_name = organization['properties']['name']
        comp_coords = comp_long, comp_lat = organization['geometry']['coordinates']
        comp_adress = organization['properties']['CompanyMetaData']['address']
        lc2, uc2 = comp_bound = organization['properties']['boundedBy']
        comp_time = organization['properties']['CompanyMetaData']['Hours']['text']

        lc1 = list(map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split()))
        uc1 = list(map(float, toponym['boundedBy']['Envelope']['upperCorner'].split()))
        lc, uc = get_max_zoom(lc1, uc1, lc2, uc2)

        toponym_longitude, toponym_lattitude = toponym_coodrinates
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": zoom_toponym_two_object(lc, uc),
            "l": "map",
            "pt": f'{",".join(toponym_coodrinates)},home~{",".join(list(map(str, comp_coords)))},pm2dbl'
        }
        toponym_longitude = float(toponym_longitude)
        toponym_lattitude = float(toponym_lattitude)

        l = count_distance(toponym_lattitude, toponym_longitude, comp_lat, comp_long)
        map_api_server = "http://static-maps.yandex.ru/1.x/"

        response = requests.get(map_api_server, params=map_params)
        with open('image.jpg', mode='wb') as f:
            f.write(response.content)

        im = Image.open('image.jpg')
        draw_text = ImageDraw.Draw(im)
        font = ImageFont.truetype('arial.ttf', size=20)
        draw_text.text(
            (10, 10),
            comp_name,
            font=font,
            fill=('#0000ff'),
        )
        draw_text.text(
            (10, 40),
            comp_adress,
            font=font,
            fill=('#0000ff'),
        )
        draw_text.text(
            (10, 70),
            comp_time,
            font=font,
            fill=('#0000ff'),
        )
        draw_text.text(
            (10, 100),
            f"Расстояние до аптеки: {l} км",
            font=font,
            fill=('#0000ff'),
        )
        im.show()
        os.remove('image.jpg')
