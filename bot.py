from random import choice, shuffle
from discord.ext import commands

predictions = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes — definitely', 'You may rely on it',
               'As I see it, yes', 'Most likely', 'Outlook good', 'Signs point to yes', 'Yes', 'Reply hazy, try again',
               'Ask again later', 'Better not tell you now', 'Cannot predict now', 'Concentrate and ask again',
               'Don’t count on it', 'My reply is no', 'My sources say no', 'Outlook not so good', 'Very doubtful']
shuffle(predictions)
questions = []
bot = commands.Bot(command_prefix='>')


@bot.event
async def on_ready():
    print(f'log in')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def h(ctx):
    await ctx.send(
        "```Welcome! I'm Discord bot and I'm very glad to see you!\n Here are some usefil commands:\n>help - it's clear I suppose\n>ping - to check bot activity\n>new voice [or 'text'] <name> - to create new channel automatically\n>predict <question> - to get a prediction on early question```")


@bot.command()
async def new(ctx, type, name):
    if type == 'voice':
        chan_2 = await ctx.guild.create_voice_channel(name=name)
    elif type == 'text':
        chan = await ctx.guild.create_text_channel(name=name)
    else:
        await ctx.send("Invalid command (or you're) Use !help")
        return
    await ctx.send('New channel was created. Check it out now!')


@bot.command()
async def predict(ctx, *que):
    global questions
    req = ' '.join(que)
    if req in questions:
        await ctx.send("You're too annoying with your silly question!!!")
    else:
        questions.append(req)
        await ctx.send(choice(predictions))


bot.run('token')
