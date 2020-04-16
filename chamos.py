#!/usr/bin/python3

import datetime
import json

import discord
import tools
import hypixel

def log(text):
    print('{0}: {1}'.format(datetime.datetime.now().strftime('%Y-%m-%d %H%M%S'), text))


class ChamosBot(discord.Client):
    async def on_ready(self):
        log('Logged in as {0}, id {1}'.format(self.user.name, self.user.id))

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!ip'):
            log('Requesting server IP')
            await message.channel.send('The *survival* server\'s ip is icecraft.hosthorde.net. This IP isn\'t going to change anytime soon! The *PVP* server\'s IP is currently {0}. Heads up, this IP tends to change!'.format(tools.get_ip()))
            log('Successfully served server IP')
        elif message.content.startswith('pls corgi'):
            log('Getting corgi gif')
            gif = await tools.get_gif('corgi')
            await message.channel.send(gif)
            await message.channel.send('https://www.danasilver.org/giphymessages/PoweredBy_Horizontal_Light-Backgrounds.gif')
            log('Successfully served corgi gif')
        elif message.content.startswith('!stats'):
            # Message should be !stats [bedwars|skywars|pit] ign ign ign
            games = ['bedwars', 'skywars', 'pit', 'bw', 'sw']
            game_string = 'Oops, looks like the game you asked for is invalid! {0} are available'.format(', '.join(games))
            log('Stats requested with "{0}"'.format(message.content))
            parameters = message.content.split()[1:]

            game = parameters[0]
            usernames  = parameters[1:]
            log('Game: {1}; Usernames: {0}'.format(', '.join(usernames), game))

            stats_page = 'http://chamosbotonline.herokuapp.com/bedwars?igns={0}'.format('.'.join(usernames))

            comparison = None
            if game.lower() in ['bedwars', 'bw']:
                comparison = str(hypixel.Bedwars(usernames))
            elif game.lower() in ['skywars', 'sw']:
                comparison = str(hypixel.Skywars(usernames))
            elif  game.lower() == 'pit':
                comparison = str(hypixel.Pit(usernames))

            final_msg  = '```\n{0}\n```'.format(comparison if game.lower() in games and comparison else game_string)
            await message.channel.send(final_msg)
            if game.lower() == 'bedwars':
                await message.channel.send(embed=discord.Embed(title='Chamosbot Online', url=stats_page, description='Check out their stats over time!'))
            log('Successfully served {1} stat comparison for {0}'.format(', '.join(usernames), game))
        elif message.content.startswith('!link'):
            parameters = message.content.split()[1:]
            usernames = parameters
            stats_page = 'http://chamosbotonline.herokuapp.com/bedwars?igns={0}'.format('.'.join(usernames))
            await message.channel.send(embed=discord.Embed(title='Chamosbot Online', url=stats_page, description='Check out their stats over time!'))
        elif message.content.startswith('!apikey'):
            await tools.register_hypixel_api_key(message, self)


    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)


discord_secret = json.loads(open('credentials.json').read())['discord-token'] 

client = ChamosBot()
client.run(discord_secret)
