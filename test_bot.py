import discord
from random import choice, shuffle


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        global questions
        data = message.content
        if message.author == self.user:
            return
        res = []
        if data[0] == '>':
            data = data[1:]
            if not data.strip():
                res = ['Invalid command. You can use !help.']
            elif data == 'ping':
                res = ['pong']
            elif data in ['help', 'h']:
                '''res = ["Welcome! I'm Discord bot and I'm very glad to see you!",
                       "Here are some usefil commands:",
                       ">help - it's clear I suppose", "!ping - to check bot activity",
                       ">new voice [or 'text'] <name> - to create new channel automatically",
                       ">predict <question> - to get a prediction on early question"]'''
                res = ["```Welcome! I'm Discord bot and I'm very glad to see you!\n Here are some usefil commands:\n>help - it's clear I suppose\n>ping - to check bot activity\n>new voice [or 'text'] <name> - to create new channel automatically\n>predict <question> - to get a prediction on early question```"]
            elif data[:3] == 'new':
                cmd = data.split()
                if len(cmd) != 3 or cmd[1] not in ['text', 'voice']:
                    res = ["Invalid command (or you're) Use !help"]
                else:
                    if cmd[1] == 'text':
                        chan = await message.guild.create_text_channel(name=cmd[2])
                    else:
                        chan_2 = await message.guild.create_voice_channel(name=cmd[2])
                    # web = await chan.create_webhook(name='New web')
                    res = ['New channel was created. Check it out now!']
            elif data.split()[0] == 'predict':
                info = data.split()
                if info[1] in questions:
                    res = ["You're too annoying with your silly question!!!"]
                else:
                    questions.append(info[1])
                    res = [choice(predictions)]
            else:
                res = ["Welcome! I'm Discord bot and I'm very glad to see you!",
                       "Here are some usefil commands:",
                       "!help - it's clear I suppose", "!ping - to check bot activity",
                       "!new voice [or 'text'] <name> - to create new channel automatically",
                       "!predict <question> - to get a prediction on early question"]
        for i in res:
            await message.channel.send(i)


predictions = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes — definitely', 'You may rely on it',
               'As I see it, yes', 'Most likely', 'Outlook good', 'Signs point to yes', 'Yes', 'Reply hazy, try again',
               'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
               'Don’t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
shuffle(predictions)
questions = []
client = MyClient()
client.run('Njc3MDg1MTM4NzUxODQ4NDY5.XkPGsg.bIVgyxLdntWrm2z2_BWr1PUWJnE')
