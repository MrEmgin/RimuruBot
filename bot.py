import discord
from discord.ext import commands
import time
import http.cookiejar as cookielib
import urllib.request
import re
import base64
from PIL import Image
from random import choice, randint, shuffle
import os
import shutil


async def search_by_url(image_path):
    cj = cookielib.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    headers = [[('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')],
               [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36')],
               [('User-agent',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')],
               [('User-agent',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')],
               [('User-agent',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')],
               [('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0')],
               [('User-agent',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36')],
               [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:72.0) Gecko/20100101 Firefox/72.0')],
               [('User-agent',
                 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')],
               [('User-agent',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')],
               [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; rv:68.0) Gecko/20100101 Firefox/68.0')],
               [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0')],
               [('User-agent',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36')],
               [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Safari/537.36')],
               [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0')],
               [('User-agent',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')],
               [('User-agent',
                 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')],
               [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0')]]
    opener.addheaders = choice(headers)

    google_path = 'http://images.google.com/searchbyimage?image_url=' + image_path
    source = opener.open(google_path).read()
    results = re.findall(r"var s='(.*?)'", source.decode('utf-8'))
    for i in results[:20]:
        t = list(str(int(time.time())) + str(randint(1000, 90000)))
        shuffle(t)
        shuffle(t)
        t = ''.join(t)

        coded_string = ''.join(i.split(r'\x')[0]).split(',')[1]
        path = f'data/{t}.jpg'
        with open(path, 'wb') as file:
            file.write(base64.decodebytes(str.encode(coded_string) + b'=='))

        ratio = 2.
        image = Image.open(path).convert('RGB')
        w, h = image.size
        image = image.resize((int(w * ratio), int(h * ratio)))
        image.save(path)


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
async def new(ctx, type, *name):
    name = '-'.join(name)
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


@bot.command()
async def search(ctx, req):
    print(req)
    if '://' in req:
        await search_by_url(req)
        files = os.listdir('./data')
        ctx.send("Here are some similar images...")
        for i in range(3):
            path = choice(files)
            print(path)
            await ctx.message.channel.send(file=discord.File('data/' + path))
        shutil.rmtree('./data')
        os.mkdir('data')
    else:
        ctx.send("Unfortunately, I can't find such image...")


bot.run('token')
