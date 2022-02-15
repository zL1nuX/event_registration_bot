import certifi
import ssl
from urllib.request import urlopen
from yandex_geocoder import Client
from config import zoom, yandex_token
from sheets import get_info

client = Client(yandex_token)
coordinates = client.coordinates(get_info()[0])

# получаем ссылку на
image_url = f"https://static-maps.yandex.ru/1.x/?ll={coordinates[0]},{coordinates[1]}&size=650,450" \
            f"&z={str(zoom)}&l=map&pt={coordinates[0]},{coordinates[1]},pm2gnm"

context = ssl.create_default_context(cafile=certifi.where())


data = urlopen(image_url, context=context).read()
