import requests
import re
import random
import json

import giphy_client as gif
from giphy_client.rest import ApiException

giphy = gif.DefaultApi()

giphy_key = json.loads(open('credentials.json').read())['giphy-api-key']

website_link = 'https://chamosbotonline.herokuapp.com'

async def register_hypixel_api_key(message, bot):
    command_format = '`!apikey <SERVER ID> <HYPIXEL API KEY>`'
    guild = message.guild
    user  = message.author
    args  = message.content.split()[1:]
    if args == []:
        # User only sent !apikey, so DM them asking for more
        await user.send('Thanks for connecting your server to ChamosBot! Please reply to this direct message with the following command: {0} For help finding these, check out {1}/commands/apikey'.format(command_format, website_link))
        if guild is not None: await user.send('btw... it looks like your server ID is {0}'.format(guild.id))
    elif len(args) == 2:
        # User sent both parameters, test and save API key
        if guild is not None:
            await user.send('I\'m processing your key, but consider deleting your message from the public guild chat, as the key should be kept private.')

        guild_id, key = args
        await user.send('Your command formatting looks perfect! I\'m testing the API key right now.')
        req = requests.get('https://api.hypixel.net/player?key={0}&name=parcerx'.format(key))
        res = req.json()
        if res['success'] is True:
            # Key works. Save it.
            await user.send('Your key is working! I\'m linking your guild to the key, and I will notify you when the registration is complete.')

            current_data = json.loads(open('credentials.json').read())
            current_data['hypixel-api-keys'][guild_id] = key
            with open('credentials.json', 'w') as credentials_file:
                credentials_file.write(json.dumps(current_data, indent=4, sort_keys=True))

            await user.send('The key is connected! Try running `!stats bedwars gamerboy80` in a text channel that ChamosBot is in!')
        elif res['success'] is False and res['cause'] == 'Invalid API key':
            await user.send('It looks like the API key you provided was incorrect. Please check the key and try the command again.')
        else:
            await user.send('It looks like something may have gone wrong on Hypixel\'s servers when testing your key. Please try again, and be sure to check the key.')
    else:
       await user.send('It seems like the command you sent didn\'t have the right parameters. Please make sure your command follows the format: {0}'.format(command_format))
       await user.send('For help, please visit {0}'.format(website_link))


def get_ip():
    page = requests.get('https://secret-forest-58202.herokuapp.com/').text
    return re.findall(r'0\.tcp\.ngrok\.io:[0-9]{5}', page)[0]


async def get_gif(query):
    try:
        giphy_token = giphy_key
        response = giphy.gifs_search_get(giphy_token, query, limit=20, rating='g')
        gifs = list(response.data)
        random.shuffle(gifs)
        return gifs[0].url
    except ApiException as e:
        return 'Uh oh, I couldn\'t grab the {0} gif...'.format(query)
