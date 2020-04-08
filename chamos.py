#!/usr/bin/python3

import datetime
import json

import discord
import tools
import hypixel

class ChamosBot(discord.Client):
    async def on_ready(self):
        print('Logged in as {0}, id {1}'.format(self.user.name, self.user.id))

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!ip'):
            print('Requesting server IP')
            await message.channel.send('The *survival* server\'s ip is icecraft.hosthorde.net. This IP isn\'t going to change anytime soon! The *PVP* server\'s IP is currently {0}. Heads up, this IP tends to change!'.format(tools.get_ip()))
            print('Successfully served server IP')
        elif message.content.startswith('pls corgi'):
            print('Getting corgi gif')
            gif = await tools.get_gif('corgi')
            await message.channel.send(gif)
            await message.channel.send('https://www.danasilver.org/giphymessages/PoweredBy_Horizontal_Light-Backgrounds.gif')
            print('Successfully served corgi gif')
        elif message.content.startswith('!stats'):
            # Message should be !stats [bedwars|skywars] ign ign ign
            print('Stats requested with "{0}"'.format(message.content))
            parameters = message.content.split()[1:]

            game = parameters[0]
            usernames  = parameters[1:]
            print('Game: {1}; Usernames: {0}'.format(', '.join(usernames), game))

            comparison = hypixel.PlayerCompare(usernames)
            final_msg  = '```\n{0}\n```'.format(comparison.bedwars() if game.lower() == 'bedwars' else comparison.skywars() if game.lower() == 'skywars' else comparison.pit() if game.lower() == 'pit' else 'Oops, looks like the game you asked for is invalid! Try "Bedwars" or "Skywars"!')
            await message.channel.send(final_msg)
            print('Successfully served {1} stat comparison for {0}'.format(', '.join(usernames), game))


    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)
            # await member.add_roles(tools.Memeber)


discord_secret = json.loads(open('credentials.json').read())['discord-token'] 

client = ChamosBot()
client.run(discord_secret)
