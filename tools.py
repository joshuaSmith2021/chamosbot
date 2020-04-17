import requests
import re
import random
import json
import datetime

import hypixel

website_link = 'https://chamosbotonline.herokuapp.com'

def log(text):
    print('{0}: {1}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H%M%S'), text))


async def get_game_stats(message, bot):
    # Message should be !stats [bedwars|skywars|pit] ign ign ign
    games = ['bedwars', 'skywars', 'pit', 'bw', 'sw']
    game_string = 'Oops, looks like the game you asked for is invalid! {0} are available'.format(', '.join(games))
    log('Stats requested with "{0}"'.format(message.content))
    parameters = message.content.split()[1:]

    try:
        api_key = json.loads(open('credentials.json').read())['hypixel-api-keys'][str(message.guild.id)]
    except KeyError as err:
        await message.channel.send('It looks like your server does not have a Hypixel API key connected! Please use command `!apikey` to get connected!')
        log('{0} did not have an API key connected'.format(message.guild))
        return

    game = parameters[0]
    usernames  = parameters[1:]
    log('Game: {1}; Usernames: {0}'.format(', '.join(usernames), game))

    stats_page = 'http://chamosbotonline.herokuapp.com/bedwars?igns={0}'.format('.'.join(usernames))

    comparison = None
    if game.lower() in ['bedwars', 'bw']:
        comparison = str(hypixel.Bedwars(usernames, apikey=api_key))
    elif game.lower() in ['skywars', 'sw']:
        comparison = str(hypixel.Skywars(usernames, apikey=api_key))
    elif  game.lower() == 'pit':
        comparison = str(hypixel.Pit(usernames, apikey=api_key))

    final_msg  = '```\n{0}\n```'.format(comparison if game.lower() in games and comparison else game_string)
    await message.channel.send(final_msg)
    #if game.lower() == 'bedwars':
    #    await message.channel.send(embed=discord.Embed(title='Chamosbot Online', url=stats_page, description='Check out their stats over time!'))
    log('Successfully served {1} stat comparison for {0}'.format(', '.join(usernames), game))


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
