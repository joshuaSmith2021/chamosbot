import requests
import re
import random

import giphy_client as gif
from giphy_client.rest import ApiException

giphy = gif.DefaultApi()

def get_ip():
    page = requests.get('https://secret-forest-58202.herokuapp.com/').text
    return re.findall(r'0\.tcp\.ngrok\.io:[0-9]{5}', page)[0]


async def get_gif(query):
    try:
        giphy_token = 'tiF0yt05LjvjDWtN3FcO0UY70NWXC9DL'
        response = giphy.gifs_search_get(giphy_token, query, limit=20, rating='g')
        gifs = list(response.data)
        random.shuffle(gifs)
        return gifs[0].url
    except ApiException as e:
        return 'Uh oh gamers, I couldn\'t grab the {0} gif...'.format(query)
