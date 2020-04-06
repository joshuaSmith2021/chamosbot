import discord
import tools

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!ip'):
            await message.channel.send('The *survival* server\'s ip is icecraft.hosthorde.net. This IP isn\'t going to change anytime soon! The *PVP* server\'s IP is currently {0}. Heads up, this IP tends to change!'.format(tools.get_ip()))
        elif message.content.startswith('pls corgi'):
            gif = await tools.get_gif('corgi')
            await message.channel.send(gif)
            await message.channel.send('https://www.danasilver.org/giphymessages/PoweredBy_Horizontal_Light-Backgrounds.gif')
        elif message.content.startswith('xfavor playlist'):
            # Send messages to tell rhythm to play the entire playlist
            pass
            

    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = 'Welcome {0.mention} to {1.name}!'.format(member, guild)
            await guild.system_channel.send(to_send)
            # await member.add_roles(tools.Memeber)


client = MyClient()
client.run('NjI1NTAxMDcyMzk5NTMyMDQy.XYmeEg.FYz9nmX0CNxJa2n3wa7e9Hoq6Sw')
