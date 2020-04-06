#!/usr/bin/python3

import logging
import datetime
import json

import discord
import tools
import hypixel

class ChamosBot(discord.Client):
    async def on_ready(self):
        logging.info('Logged in as {0}, id {1}'.format(self.user.name, self.user.id))

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!ip'):
            logging.debug('Requesting server IP')
            await message.channel.send('The *survival* server\'s ip is icecraft.hosthorde.net. This IP isn\'t going to change anytime soon! The *PVP* server\'s IP is currently {0}. Heads up, this IP tends to change!'.format(tools.get_ip()))
            logging.info('Successfully served server IP')
        elif message.content.startswith('pls corgi'):
            logging.debug('Getting corgi gif')
            gif = await tools.get_gif('corgi')
            await message.channel.send(gif)
            await message.channel.send('https://www.danasilver.org/giphymessages/PoweredBy_Horizontal_Light-Backgrounds.gif')
            logging.info('Successfully served corgi gif')
        elif message.content.startswith('!stats'):
            # Message should be !stats bedwars ign ign ign
            logging.debug('Stats requested with "{0}"'.format(message.content))
            usernames  = message.content.split()[2:]
            logging.debug('Usernames: {0}'.format(', '.join(usernames)))
            comparison = hypixel.PlayerCompare(usernames)
            final_msg  = '```\n{0}\n```'.format(comparison.bedwars())
            await message.channel.send(final_msg)
            logging.info('Successfully served stat comparison for {0}'.format(', '.join(usernames)))


    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)
            # await member.add_roles(tools.Memeber)


logging.basicConfig(filename='logs/{0}.log'.format(datetime.datetime.now().strftime('%Y%m%d')), level=logging.DEBUG)

discord_secret = json.loads(open('credentials.json').read())['discord-token'] 

client = ChamosBot()
client.run(discord_secret)
